import click
import libcst as cst
from libcst.display import dump
from libcst.metadata import MetadataWrapper, PositionProvider
import os

from IndentationTransformer import IndentationTransformer
from SpacesTransformer import SpacesTransformer 
from VariableNameVisitor import VariableNameVisitor 


class BlankLineTransformer(cst.CSTTransformer):
    def leave_TrailingWhitespace(self, old_node, new_node):
        return new_node.with_changes(whitespace=cst.SimpleWhitespace(value=""))

def main(filename, **kwargs):
    abs_path = os.path.abspath(filename)

    with open(filename, "r") as f:
        tree = cst.parse_module(f.read())
        if kwargs["tree"]:
            print(tree)
            exit()
    transformers = [
        IndentationTransformer(kwargs["indent"]),
        SpacesTransformer(),
    ]
    visitors = [
        # VariableNameVisitor(3),
    ]
    for t in transformers:
        tree = tree.visit(t)
    tree = MetadataWrapper(tree)
    for v in visitors:
        tree.visit(v)
        v.print_warnings(abs_path)

    if not kwargs["silent"]:
        print((tree.module.code))


if __name__ == "__main__":
    cmd = click.Command(
        name="linter",
        callback=main,
        params=[
            click.Argument(["filename"], required=True),
            click.Option(["--indent", "-i"], default=4, type=int, help="Indent"),
            click.Option(["--complexity-limit", "-c"], default=10, type=int, help="Limit"),
            click.Option(
                [
                    "--ignore-imports",
                ],
                is_flag=True,
                default=False,
            ),
            click.Option(
                [
                    "--tree",
                ],
                is_flag=True,
                default=False,
            ),
            click.Option(
                [
                    "--silent",
                ],
                is_flag=True,
                default=False,
            ),
        ],
    )
    cmd.main()
