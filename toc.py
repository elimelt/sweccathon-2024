import argparse
from pathlib import Path
import mistletoe
from mistletoe.ast_renderer import ASTRenderer
from types import SimpleNamespace
import json

colors = {
	'red': '\033[91m',
	'green': '\033[92m',
	'yellow': '\033[93m',
	'blue': '\033[94m',
	'purple': '\033[95m',
	'end': '\033[0m'
}

TAB = "  "
FILENAME = "blue"
TABLE_OF_CONTENTS = "purple"
WELCOME = "red"

def welcome():
	msg = r"""
  ______      __    __              ____   ______            __             __
 /_  __/___ _/ /_  / /__     ____  / __/  / ____/___  ____  / /____  ____  / /______
  / / / __ `/ __ \/ / _ \   / __ \/ /_   / /   / __ \/ __ \/ __/ _ \/ __ \/ __/ ___/
 / / / /_/ / /_/ / /  __/  / /_/ / __/  / /___/ /_/ / / / / /_/  __/ / / / /_(__  )
/_/  \__,_/_.___/_/\___/   \____/_/     \____/\____/_/ /_/\__/\___/_/ /_/\__/____/
	"""

	print_c(msg, WELCOME)

def print_c(text, color):
	print(f"{colors[color]}{text}{colors['end']}")

def parse(text):
	# Parse into AST JSON
	astjson = mistletoe.markdown(text, ASTRenderer)

	# Parse JSON into an object with attributes corresponding to dict keys.
	ast = json.loads(astjson, object_hook=lambda d: SimpleNamespace(**d))
	return ast


def table_of_contents(ast, output_func, depth):
	for child in ast.children:
		if child.type == "Heading" and len(child.children) == 1:
			if child.level < depth:
				continue
			output_func(child)


def get_md_paths_recursive(base_path) -> list[Path]:
	base_path = Path(base_path)
	md_paths = []
	for path in base_path.rglob("*.md"):
		md_paths.append(path)
	return md_paths


def main(args):
	noop = lambda x: x
	indent = lambda child: child.level if not args.no_path else child.level - 1
	out = lambda child: print_c(TAB * (indent(child)) + f"- {child.children[0].content}", TABLE_OF_CONTENTS)
	pathout = lambda path: print_c(f'- {path}', FILENAME) if not args.no_path else noop
	if args.format == "md":
		out = lambda child: print(TAB * (indent(child)) + f"- [{child.children[0].content}](#{child.children[0].content.lower().replace(' ', '-')})")
		pathout = lambda path: print(f'- [{path}]({path})') if not args.no_path else noop
	elif args.format == "yaml":
		out = lambda child: print(f"{TAB * (indent(child))}- {child.children[0].content}")
		pathout = lambda path: print(f'- {path}') if not args.no_path else noop


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
			pathout(md_path)
			table_of_contents(ast, out, args.depth)
			print()


if __name__ == "__main__":
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
	parser.add_argument(
		"-f",
		"--format",
		choices=["yaml", "md", "console"],
		default="console",
		help="Output format for the table of contents"
	)
	parser.add_argument(
		"-d",
		"--depth",
		type=int,
		help="Minimum heading level to include in the table of contents"
	)
	parser.add_argument(
		"--no-path",
		action="store_true",
		help="Do not print the path of the input markdown files"
	)

	args = parser.parse_args()

	if args.format == "console":
		welcome()

	main(args)
