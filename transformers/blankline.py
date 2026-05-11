import libcst as cst


class BlankLineTransformer(cst.CSTTransformer):
    def _apply_spacing(self, body, is_global):
        new_body = list(body)
        for i, node in enumerate(new_body):
            is_big = isinstance(node, (cst.FunctionDef, cst.ClassDef))
            prev_is_big = isinstance(new_body[i - 1], (cst.FunctionDef, cst.ClassDef))

            if is_global:
                count = 2 if (is_big or prev_is_big) else 0
            else:
                count = 1 if is_big else 0

            if hasattr(node, "leading_lines"):
                new_lines = [cst.EmptyLine(indent=False)] * count if i != 0 else []

                lines = node.leading_lines
                indices = [i for i, l in enumerate(lines) if l.comment]
                old_lines = lines[min(indices) : max(indices) + 1] if indices else []
                new_lines.extend(old_lines)

                new_body[i] = node.with_changes(leading_lines=new_lines)
            if is_big:
                new_body[i] = new_body[i].with_changes(lines_after_decorators=[])

        return new_body

    def leave_Module(self, old_node, new_node):
        return new_node.with_changes(
            body=self._apply_spacing(new_node.body, is_global=True),
            header=[],
            footer=[],
            has_trailing_newline=True,
        )

    def leave_IndentedBlock(self, old_node, new_node):
        return new_node.with_changes(body=self._apply_spacing(new_node.body, is_global=False))

    def leave_EmptyLine(self, old_node, new_node):
        if not new_node.comment:
            new_node = new_node.with_changes(indent=False)
        return new_node
