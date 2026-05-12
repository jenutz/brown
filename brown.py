#!/usr/bin/env python3

import libcst as cst
import click
import os
import sys

from transformers.indentation import IndentationTransformer
from transformers.whitespace import SpacesTransformer
from transformers.blankline import BlankLineTransformer


def format_code(code, **kwargs):
    transformers = [
        IndentationTransformer(kwargs.get("indent", 4)),
        SpacesTransformer(),
        BlankLineTransformer(),
    ]
    tree = cst.parse_module(code)

    for t in transformers:
        tree = tree.visit(t)

    return tree.code


def main(filename, **kwargs):
    with open(filename, "r") as f:
        source_code = f.read()

    if kwargs["tree"]:
        print(cst.parse_module(source_code))
        return

    try:
        formatted_code = format_code(source_code, **kwargs)
    except cst.ParserSyntaxError as e:
        click.secho(
            f'Error in file "{filename}", line {e.raw_line}, col {e.raw_column}:',
            fg="white",
            err=True,
        )
        click.secho(f"Syntax Error: {e.message}", fg="red", bold=True, err=True)
        sys.exit(1)

    except Exception as e:
        click.secho(f"Internal Error:", fg="white", bold=True, err=True)
        click.secho(f"[{type(e).__name__}]: {e}", fg="red", err=True)
        sys.exit(1)

    if kwargs["res_tree"]:
        print(cst.parse_module(formatted_code))
        return

    if kwargs["dry_run"]:
        print(formatted_code)
        return

    with open(filename, "w") as f:
        f.write(formatted_code)

    click.secho("Success!", fg="green", bold=True)
    click.echo(f"Formatted {click.format_filename(filename)}")


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
                ["--dry-run", "-d"],
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
