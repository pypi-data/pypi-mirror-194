try:
    from graphviz import Digraph

    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
from pycparser import c_ast


class DotVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.parent = []
        self.root = None
        self.nodeNumber = 0
        self.nodeDict = dict()
        self.g = Digraph("G")

    def _label(self, node):
        return "%s %s" % (str(self.nodeDict[node]), str(node.__class__.__name__))

    def generic_visit(self, node):
        myNodeNumber = self.nodeNumber
        self.nodeNumber += 1
        self.nodeDict[node] = str(myNodeNumber)
        self.g.node(self._label(node))
        if self.parent:
            self.g.edge(self._label(self.parent[-1]), self._label(node))
        else:
            self.root = node
        self.parent.append(node)
        for c in node:
            self.visit(c)
        self.parent.pop()

    def get_graph(self):
        return self.g


def pprint(obj, line_length=100):
    import black

    mode = black.FileMode(line_length=line_length)
    fast = False
    out = black.format_file_contents(obj.__repr__(), fast=fast, mode=mode)
    print(out)
