import libcst as cst
from libcst.metadata import MetadataWrapper, PositionProvider


class VariableNameVisitor(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self, minimalVariableName: int):
        self.min_len = minimalVariableName
        self.warnings = []

    def print_warnings(self, abs_path):
        for line, col, name in self.warnings:
            click.secho(f"{abs_path}:{line}:{col}", fg="cyan", underline=True, nl=False)
            click.echo(": ", nl=False)
            click.echo(f"Warning Variable '{name}' is too short.")

    def visit_Assign(self, node: cst.Assign):
        if targets := getattr(node, "targets"):
            for t in targets:
                t = t.target
                match t:
                    case cst.Name(value=name):
                        if len(name) < self.min_len:
                            pos = self.get_metadata(PositionProvider, node)
                            line = pos.start.line
                            column = pos.start.column
                            self.warnings.append([line, column, name])
                    case _:
                        # print(t)
                        # raise NotImplementedError()
                        pass