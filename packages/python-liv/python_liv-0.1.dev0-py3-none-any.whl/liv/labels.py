from collections.abc import Iterable

from pycparser import c_ast


class NodeLabellingVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.node_counter = 0

    def generic_visit(self, node: c_ast.Node):
        result = dict()
        result[node] = self.node_counter
        self.node_counter += 1
        if isinstance(node, Iterable):
            c: c_ast.Node
            for c in node:
                result.update(self.visit(c))
        return result

    def visit(self, node: c_ast.Node):
        # ensure type-safety, we always want to return a dict()
        return super().visit(node) or dict()
