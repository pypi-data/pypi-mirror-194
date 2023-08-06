from pycparser import c_ast


class Block:
    pass


class SegmentBlock(Block):
    def __init__(self, nodes):
        self.nodes = nodes

    def __repr__(self):
        return "SegmentBlock(%s)" % (self.__repr_nodes__())

    def __repr_nodes__(self):
        start = self.nodes[0]
        if (
            self.nodes == list(range(min(self.nodes), max(self.nodes) + 1))
            and sorted(self.nodes) == self.nodes
        ):
            return "range(%s,%s)" % (min(self.nodes), max(self.nodes) + 1)
        else:
            return self.nodes.__repr__()

    def __iter__(self):
        return iter(list())


class CompositeBlock(Block):
    def __init__(self, node_id, kind, children):
        self.node_id = node_id
        self.kind = kind
        self.children = children

    def __repr__(self):
        return "CompositeBlock(node_id = %s, kind = %s, children = %s)" % (
            self.node_id,
            self.kind,
            self.children,
        )

    def __iter__(self):
        for child in self.children:
            yield child


class BlockStructureGenerator(c_ast.NodeVisitor):
    def __init__(self, coord_to_label, coords):
        self.coord_to_label = coord_to_label
        self.coords = coords
        self.roots = list()
        self.childrenstack = list()
        self.currentsegment = list()

    def get_label(self, node):
        return self.coord_to_label[self.coords(node)]

    def _finish_segment(self):
        if self.currentsegment:
            self.childrenstack[-1].append(SegmentBlock(self.currentsegment))
        self.currentsegment = list()

    def visit_FileAST(self, node):
        print("FileAST")
        self._finish_segment()
        self.childrenstack.append(list())
        self._visit_children(node)
        self._finish_segment()
        self.roots.append(
            CompositeBlock(self.get_label(node), "FileAST", self.childrenstack.pop())
        )

    def visit_FuncDef(self, node):
        print("FuncDef")
        self._finish_segment()
        self.childrenstack.append(list())
        if node.decl is not None:
            self.visit(node.decl)
            self._finish_segment()
        if node.body is not None:
            self.visit(node.body)
            self._finish_segment()
        myself = CompositeBlock(
            self.get_label(node), "FuncDef", self.childrenstack.pop()
        )
        self.childrenstack[-1].append(myself)

    def visit_While(self, node):
        print("While")
        self._finish_segment()
        self.childrenstack.append(list())
        if node.cond is not None:
            self.visit(node.cond)
            self._finish_segment()
        if node.stmt is not None:
            self.visit(node.stmt)
            self._finish_segment()
        myself = CompositeBlock(self.get_label(node), "While", self.childrenstack.pop())
        self.childrenstack[-1].append(myself)

    def enter_default(self, node):
        self.currentsegment.append(self.get_label(node))

    def leave_default(self, node):
        pass

    def generic_visit(self, node):
        self.enter_default(node)
        self._visit_children(node)
        self.leave_default(node)

    def _visit_children(self, node):
        for child in node:
            self.visit(child)


class BlockVisitor(object):
    def visit(self, block):
        if isinstance(block, SegmentBlock):
            name = "segment"
        elif isinstance(block, CompositeBlock):
            name = block.kind
        else:
            raise TypeError("Unknown block type %s", type(block))
        method = "visit_" + name
        visitor = getattr(self, method, self.generic_visit)
        return visitor(block)

    def generic_visit(self, block):
        """Called if no explicit visitor function exists for a
        node. Implements preorder visiting of the node.
        """
        for c in block:
            self.visit(c)


class NodesFromBlockCollector(BlockVisitor):
    def __init__(self):
        self.nodelist = list()

    def generic_visit(self, block):
        if isinstance(block, SegmentBlock):
            return block.nodes
        elif isinstance(block, CompositeBlock):
            nodes = list()
            nodes.append(block.node_id)
            for child in block.children:
                nodes.extend(self.visit(child))
            return nodes

    def visit(self, block):
        return super().visit(block) or list()
