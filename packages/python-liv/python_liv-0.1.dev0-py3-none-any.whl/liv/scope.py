from pycparser import c_ast, c_generator

from liv.blocks import BlockVisitor
from liv.compat import is_FuncDecl


class ScopeCollectingVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.currentfunction = None
        self.globalvariables = dict()
        self.localvariables = dict()
        self.locmap = dict()
        self.locmap["global"] = dict()
        self.locmap["local"] = dict()

    def visit_Decl(self, node):
        print(
            "%10s: %s"
            % (
                self.currentfunction.decl.name if self.currentfunction else "Global",
                c_generator.CGenerator().visit(node),
            )
        )
        if is_FuncDecl(node.type):
            self._visit_children(node)
        elif isinstance(node.type, c_ast.TypeDecl) or isinstance(
            node.type, c_ast.PtrDecl
        ):
            name = node.name
            if not self.currentfunction:
                self.globalvariables[name] = node
            else:
                assert name not in self.localvariables
                self.localvariables[name] = node
        else:
            raise TypeError("Unknown declaration type %s", type(node.type))

    def visit_FuncDef(self, node):
        self.currentfunction = node
        self.localvariables = dict()
        result = self.generic_visit(node)
        self.currentfunction = None

    def generic_visit(self, node):
        self.locmap["global"][node] = dict(self.globalvariables)
        self.locmap["local"][node] = dict(self.localvariables)
        self._visit_children(node)

    def _visit_children(self, node):
        for child in node:
            self.visit(child)

    def get_scope_resolver(self):
        return ScopeResolver(self.locmap)


class ScopeResolver:
    def __init__(self, locmap):
        self.locmap = locmap

    def at(self, node):
        result = dict()
        if node in self.locmap["global"]:
            result.update(self.locmap["global"][node])
        if node in self.locmap["local"]:
            result.update(self.locmap["local"][node])
        return result


class ScopeAddingVisitor(BlockVisitor):
    def __init__(self, coord_to_label, scope):
        self.coord_to_label = coord_to_label
        self.label_to_coord = {v: k for k, v in coord_to_label.items()}
        self.scope = scope

    def _transfer_scope(self, name, node, block):
        block.scope = self.scope.at(node)
        if node:
            print(
                "%9s(@%-2s), vars = %s"
                % (
                    name,
                    block.node_id if hasattr(block, "node_id") else block.nodes[0],
                    ", ".join(self.scope.at(node).keys()),
                )
            )

    def visit_segment(self, block):
        node = self.label_to_coord[block.nodes[0]]
        self._transfer_scope("segment", node, block)

    def generic_visit(self, block):
        node = self.label_to_coord[block.node_id]
        self._transfer_scope(block.kind, node, block)
        super().generic_visit(block)
