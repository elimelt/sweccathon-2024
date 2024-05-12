import argparse
from pathlib import Path
import mistletoe
from mistletoe.ast_renderer import ASTRenderer
from types import SimpleNamespace
import json


def parse(text):
    # Parse into AST JSON
    astjson = mistletoe.markdown(text, ASTRenderer)

    # Parse JSON into an object with attributes corresponding to dict keys.
    ast = json.loads(astjson, object_hook=lambda d: SimpleNamespace(**d))
    return ast


def table_of_contents(ast):
    for child in ast.children:
        if child.type == "Heading" and len(child.children) == 1:
            print("\t" * (child.level) + f"- {child.children[0].content}")


def get_md_paths_recursive(base_path) -> list[Path]:
    base_path = Path(base_path)
    md_paths = []
    for path in base_path.rglob("*.md"):
        md_paths.append(path)
    return md_paths


def main():
    parser = argparse.ArgumentParser(
        description="Generate a table of contents for markdown files"
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="List of paths to markdown files or directories containing markdown files",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Search directories recursively for markdown files",
    )
    args = parser.parse_args()

    markdown_paths = []
    for path in args.paths:
        if args.recursive:
            if Path(path).is_dir():
                markdown_paths.extend(get_md_paths_recursive(path))
            else:
                print(
                    f"Warning: {path} is not a directory. Recursive option will be ignored for this path."
                )
                markdown_paths.append(Path(path))
        else:
            markdown_paths.append(Path(path))

    for md_path in markdown_paths:
        with open(md_path, "r", encoding="utf-8") as file:
            md_content = file.read()
            ast = parse(md_content)
            print(f"- {md_path}")
            table_of_contents(ast)
            print()


if __name__ == "__main__":
    main()
