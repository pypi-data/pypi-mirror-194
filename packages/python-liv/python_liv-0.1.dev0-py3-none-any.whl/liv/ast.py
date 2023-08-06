import copy

from pycparser import c_ast


# we take some inspiration in to how to copy ASTs from here
# https://stackoverflow.com/a/60234404
def iter_fields(node):
    # this doesn't look pretty because `pycparser` decided to have structure
    # for AST node classes different from stdlib ones
    index = 0
    children = node.children()
    while index < len(children):
        name, child = children[index]
        try:
            bracket_index = name.index("[")
        except ValueError:
            yield name, child
            index += 1
        else:
            name = name[:bracket_index]
            child = getattr(node, name)
            index += len(child)
            yield name, child


class DuplicatingNodeTransformer(c_ast.NodeVisitor):
    def generic_visit(self, node):
        new_node = copy.copy(node)
        for field, old_value in iter_fields(new_node):
            if isinstance(old_value, list):
                new_values = []
                for value in old_value:
                    if isinstance(value, c_ast.Node):
                        value = self.visit(value)
                        if value is None:
                            continue
                        elif not isinstance(value, c_ast.Node):
                            new_values.extend(value)
                            continue
                    new_values.append(value)
                setattr(new_node, field, new_values)
            elif isinstance(old_value, c_ast.Node):
                new_field_node = self.visit(old_value)
                setattr(new_node, field, new_field_node)
        return new_node


class DuplicatingFilteringNodeTransformer(DuplicatingNodeTransformer):
    def __init__(self, whitelist):
        self.whitelist = whitelist

    def generic_visit(self, node):
        if node not in self.whitelist:
            return None
            # children = [super(DuplicatingFilteringNodeTransformer,self).generic_visit(c) for c in node if c in self.whitelist]
            # if len(children)>0:
            #    return children[0]
            # else:
        else:
            return super().generic_visit(node)
