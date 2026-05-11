import libcst as cst


class IndentationTransformer(cst.CSTTransformer):
    def __init__(self, indent: int):
        self.indent = indent

    def leave_IndentedBlock(self, old_node, new_node):
        return new_node.with_changes(indent=" " * self.indent)
