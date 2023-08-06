from typing import List, Optional, Union

from pycparser import c_ast
from pycparser.plyparser import Coord

from liv.ast import DuplicatingFilteringNodeTransformer
from liv.blocks import Block, BlockVisitor, CompositeBlock, NodesFromBlockCollector
from liv.compat import CParser, call
from liv.invariant import Invariant
from liv.labels import NodeLabellingVisitor


class ProgramSlicingVisitor(BlockVisitor):
    def __init__(
        self,
        coord_to_label,
        conditions=dict(),
        loop_invariants: List[Invariant] = list(),
    ):
        self.coord_to_label = coord_to_label
        self.label_to_coord = {v: k for k, v in coord_to_label.items()}
        self.conditions = conditions
        self.currentprogram: List[Union[Block, c_ast.Node]] = list()
        self.programs: List[List[Union[Block, c_ast.Node]]] = list()
        self.in_main = False
        self.context = list()
        self.loop_invariants = loop_invariants

    def get_slices(self):
        return self.programs

    def visit_segment(self, block):
        if self.in_main:
            self.currentprogram.append(block)
        else:
            self.context.append(block)

    def _finish_program(self):
        self.programs.append(self.currentprogram)
        self.currentprogram = list()

    def _init_scope(self, block):
        scope = block.scope
        for variable, decl in scope.items():
            self.currentprogram.append(nondet_initialize(decl))

    def visit_FuncDef(self, block):
        if self.label_to_coord[block.node_id].decl.name == "main":
            self.in_main = True
            self.currentprogram = list()
            self.programs = list()
            self._init_scope(block)
            func_decl = self.label_to_coord[block.children[0].nodes[0]].type
            for decl in func_decl.args or []:
                self.currentprogram.append(nondet_initialize(decl))
            for c in block.children[1:]:
                self.visit(c)
            self._finish_program()
        else:
            self.in_main = False
            self.context.append(block)

    def visit_While(self, block: CompositeBlock):
        coord: Coord = self.label_to_coord[block.node_id].coord
        invariant: Optional[str] = None
        for inv in self.loop_invariants:  # todo: improve scaling
            if inv.coord.line == coord.line:  # todo: improve matching
                invariant = inv.formula
        self.assert_(invariant)
        self._finish_program()

        self._init_scope(block)
        self.assume(invariant)
        cond = block.children[0]
        self.currentprogram.append(
            assume(self.label_to_coord[cond.nodes[0]])
        )  # todo: actually copy the condition segment before maybe, you never know
        for c in block.children[1:]:
            self.visit(c)
        self.assert_(invariant)
        self._finish_program()

        self._init_scope(block)
        self.assume(invariant)
        self.currentprogram.append(assume(not_(self.label_to_coord[cond.nodes[0]])))

    def assume(self, text: Optional[str]):
        if text:
            self.currentprogram.append(assume(formula_to_ast(text)))

    def assert_(self, text: Optional[str]):
        if text:
            self.currentprogram.append(assert_(formula_to_ast(text)))


def formula_to_ast(
    text,
):  # todo: conjunct parts if invariant is in x>0;y<0 form which is allowed in SV-COMP
    parser = CParser()
    ast: c_ast.FileAST = parser.parse("int main() {(%s);}" % text)
    funcdef: c_ast.FuncDef = ast.ext[0]
    compound: c_ast.Compound = funcdef.body
    return compound.block_items[0]


def nondet_initialize(decl):
    # print(decl)
    if isinstance(decl.type, c_ast.TypeDecl):
        type_ = decl.type.type
        names = type_.names
    elif isinstance(decl.type, c_ast.PtrDecl):
        names = ["pointer"]
    else:
        assert False
    fct_name = "__VERIFIER_nondet_%s" % (_names_to_sig(names))
    fun_call = c_ast.FuncCall(name=c_ast.ID(fct_name), args=c_ast.ExprList(list()))
    result = call(
        c_ast.Decl,
        name=decl.name,
        quals=decl.quals,
        align=decl.align if hasattr(decl, "align") else None,
        storage=decl.storage,
        funcspec=decl.funcspec,
        type=decl.type,
        init=fun_call,
        bitsize=decl.bitsize,
        coord=None,
    )
    return result


def _names_to_sig(names):
    for defining_name in ["int", "long", "char", "double", "float", "bool", "pointer"]:
        if defining_name in names:
            return defining_name
    if len(names) == 1:
        if "signed" in names[0]:
            return "int"
    print(names)
    assert False


def _handle(cond, fname) -> c_ast.Node:
    return c_ast.FuncCall(
        name=c_ast.ID(fname),
        args=c_ast.ExprList(
            [
                cond,
            ]
        ),
    )


def assume(cond) -> c_ast.Node:
    return _handle(cond, "LIV_assume")


def assert_(cond) -> c_ast.Node:
    return _handle(cond, "LIV_assert")


def not_(cond):
    return c_ast.BinaryOp("==", cond, c_ast.Constant("int", "0"))


def synthesize(label_to_node, prog):
    body = []
    for part in prog:
        if isinstance(part, Block):
            nfbc = NodesFromBlockCollector()
            nodes = nfbc.visit(part)
            body.append(
                DuplicatingFilteringNodeTransformer(
                    [label_to_node[node] for node in nodes]
                ).visit(label_to_node[nodes[0]])
            )
        else:
            body.append(part)
    return body


def create_main(statements):

    # hack for getting rid of a compound block at the beginning of main
    # TODO: properly handle scoping/ Compound blocks
    newstatements = list()
    afterdecls = False
    for s in statements:
        if not isinstance(s, c_ast.Decl) and not afterdecls:
            afterdecls = True
            if isinstance(s, c_ast.Compound):
                for child in s:
                    newstatements.append(child)
            else:
                newstatements.append(s)
        else:
            newstatements.append(s)

    rettype = call(
        c_ast.TypeDecl,
        declname="_hidden",
        quals=[],
        align=None,
        type=c_ast.IdentifierType(["int"]),
    )
    mainfuncdecl = c_ast.FuncDecl(
        args=c_ast.ParamList([]),
        type=call(
            c_ast.TypeDecl,
            declname="main",
            align=None,
            coord=None,
            quals=None,
            type=rettype,
        ),
    )
    maindecl = call(
        c_ast.Decl,
        name="main",
        quals=[],
        align=None,
        bitsize=None,
        coord=None,
        funcspec=None,
        init=None,
        storage=None,
        type=mainfuncdecl,
    )
    return c_ast.FuncDef(
        maindecl,
        None,
        c_ast.Compound(newstatements),
    )


def instrumentation_declarations():
    return """extern void abort (void);
extern int __VERIFIER_nondet_int();
extern _Bool __VERIFIER_nondet_bool();
extern void * __VERIFIER_nondet_pointer();
void LIV_assert(int cond) {
  if (!cond) reach_error();
}
void LIV_assume(int cond) {
  if (!cond) abort();
}
"""
