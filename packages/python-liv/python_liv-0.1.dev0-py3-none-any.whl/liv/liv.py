import argparse
import glob
import os
import sys
from os.path import realpath
from pathlib import Path

from pycparser import c_ast

for whl in glob.glob(
    str(Path(realpath(__file__)).parent.parent.joinpath("lib", "python", "*.whl"))
):
    sys.path.insert(0, whl)


from liv import __version__
from liv.blocks import BlockStructureGenerator
from liv.compat import PCYPARSEREXT, CGenerator, CParser
from liv.invariant import load_loop_invariants
from liv.labels import NodeLabellingVisitor
from liv.preprocess import remove_comments, rewrite_cproblem
from liv.programgeneration import (
    ProgramSlicingVisitor,
    create_main,
    instrumentation_declarations,
    synthesize,
)
from liv.scope import ScopeAddingVisitor, ScopeCollectingVisitor
from liv.util import setup_cache_handling
from liv.verifier import get_verifier
from liv.visualization import GRAPHVIZ_AVAILABLE, DotVisitor

sys.dont_write_bytecode = True  # prevent creation of .pyc files


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        action="version",
        version="{}".format(__version__),
    )
    parser.add_argument(
        "--property",
        required=True,
        help="The property",
        metavar="PROPERTY",
    )
    parser.add_argument(
        "--data-model",
        help="The data-model, currently supported: ILP32 and LP64",
        default="LP64",
        metavar="DATAMODEL",
    )
    parser.add_argument(
        "--verifier",
        help="The cvt actor definition for the verifiers to use in the verification backend",
        metavar="VERIFIER",
        default="actors/cpachecker.yml",
    )
    parser.add_argument(
        "--verifierversion",
        help="The version of the specified backend verifier actor that shall be used",
        metavar="VERIFIERVERSION",
    )
    parser.add_argument(
        "--outputdir",
        help="The output directory",
        metavar="OUTPUTDIR",
        default="output",
    )
    parser.add_argument(
        "--witness",
        help="The input witness",
        metavar="WITNESS",
    )
    parser.add_argument(
        "--loglevel",
        default="warning",
        choices=["critical", "error", "warning", "info", "debug"],
        help="Desired verbosity of logging output. "
        "Only log messages at or above the specified level are displayed.",
        metavar="LOGLEVEL",
    )
    parser.add_argument(
        "program",
        help="The program.",
        metavar="PROGRAM",
    )
    parser.add_argument(
        "--cache-dir",
        help="The directory to put files that are cached",
        metavar="CACHE_DIR",
    )
    parser.add_argument(
        "--no-cache-update",
        help="Prevent caches from being updated",
        action="store_false",
    )
    return parser


def coords(node):
    return node


def outputfile(args, name: str):
    os.makedirs(args.outputdir, exist_ok=True)
    return os.path.join(args.outputdir, name)


def main(argv):
    parser = create_arg_parser()
    args = parser.parse_args(argv)
    for entry in vars(args):
        print(entry)
        print(getattr(args, entry))
    print("main")

    setup_cache_handling(args)

    loop_invariants = list()
    if args.witness:
        loop_invariants = load_loop_invariants(args.witness)

    text = open(args.program, "r").read()
    if not PCYPARSEREXT:
        text = rewrite_cproblem(text)
    else:
        text = remove_comments(text)
    print(text)
    parser = CParser()
    ast = parser.parse(text, filename=args.program)

    if GRAPHVIZ_AVAILABLE:
        d = DotVisitor()
        d.visit(ast)
        d.get_graph().save(outputfile(args, "ast.dot"))

    coord_to_label = NodeLabellingVisitor().visit(ast)
    b = BlockStructureGenerator(coord_to_label, coords)
    b.visit(ast)

    print("SCOPING")
    s = ScopeCollectingVisitor()
    assert len(b.roots) == 1
    s.visit(ast)
    scope = s.get_scope_resolver()

    print("SCOPEADDING")
    ScopeAddingVisitor(coord_to_label, scope).visit(b.roots[0])

    print("PROGRAMVISITING")
    p = ProgramSlicingVisitor(coord_to_label, loop_invariants=loop_invariants)
    p.visit(b.roots[0])

    bodies = list()
    generator = CGenerator()
    label_to_coord = {v: k for k, v in coord_to_label.items()}

    contextparts = synthesize(label_to_coord, p.context)

    print(generator.visit(c_ast.FileAST(contextparts)))
    for prog in p.get_slices():
        bodies.append(synthesize(label_to_coord, prog))

    generated_programs = list()
    for body in bodies:
        whole_program = c_ast.FileAST(contextparts + [create_main(body)])
        generated_programs.append(
            instrumentation_declarations() + generator.visit(whole_program)
        )
    for i, p in enumerate(generated_programs):
        print("#" * 20)
        print(p)
        with open(outputfile(args, "program_%d.c" % ((i + 1),)), "w") as f:
            f.write(p)
    print("Generated %d programs" % len(generated_programs))

    verifier = get_verifier(args)

    results = list()
    for i, p in enumerate(generated_programs):
        program_path = outputfile(args, "program_%d.c" % (i + 1))
        res = verifier.verify(
            program_path,
            specification=args.property,
            data_model=args.data_model,
        )
        results.append(res)
        print(f"{program_path}: {res['verdict']}")
    verdicts = [str(r["verdict"]) for r in results]
    print("Overall result:")
    if any([v.startswith("false") for v in verdicts]):
        print("false")
    elif all([v == "true" for v in verdicts]):
        print("true")
    else:
        print("unknown")

    # print(p.context)


if __name__ == "__main__":
    main(sys.argv[1:])
