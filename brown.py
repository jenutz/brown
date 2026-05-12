import libcst as cst
import click
import os

from transformers.indentation import IndentationTransformer
from transformers.whitespace import SpacesTransformer
from transformers.blankline import BlankLineTransformer

def format_code(code, **kwargs):
    transformers = [
        IndentationTransformer(kwargs["indent"]),
        SpacesTransformer(),
        BlankLineTransformer(),
    ]

    tree = cst.parse_module(code)
    for t in transformers:
        tree = tree.visit(t)
    
    return tree.code

def main(filename, **kwargs):
    abs_path = os.path.abspath(filename)

    with open(filename, "r") as f:
        code = f.read()

    if kwargs["tree"]:
        print(cst.parse_module(code))
        exit()

    code = format_code(code, **kwargs)

    if kwargs["dry_run"]:
        print(code)
    elif kwargs["res_tree"]:
        print(cst.parse_module(code))
    else:
        with open(filename, "w") as f:
            f.write(code)


if __name__ == "__main__":
    cmd = click.Command(
        name="Brown",
        callback=main,
        params=[
            click.Argument(["filename"], type=click.Path(exists=True)),
            click.Option(
                ["--indent", "-i"],
                default=4,
                type=int,
                help="Number of spaces to use for indentation levels.",
            ),
            click.Option(
                ["--dry-run"],
                is_flag=True,
                default=False,
                help="Output the formatted code to terminal (stdout) without modifying the original file.",
            ),
            click.Option(
                ["--tree"],
                is_flag=True,
                default=False,
                help="DEBUG: Print the LibCST parse tree of the source file and exit.",
            ),
            click.Option(
                ["--res-tree"],
                is_flag=True,
                default=False,
                help="DEBUG: Print the LibCST parse tree of the resulting formatted code and exit.",
            ),
        ],
    )
    cmd.main()