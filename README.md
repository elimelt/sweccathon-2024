# Markdown Table of Contents Generator

This is a command-line tool developed for the Productivity track of SWECCathon 2024. It generates a table of contents for Markdown files, making it easier to navigate through large documents in the terminal.

## Table of Contents

(you better believe I generated this with `toc`)

- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Example](#example)
  - [Reference](#reference)

## Overview

The Markdown Table of Contents Generator is a Python script that parses Markdown files and generates a table of contents based on the headings in the document. It uses the `mistletoe` library to parse Markdown syntax into an Abstract Syntax Tree (AST) and then extracts headings to create the table of contents.

## Features

- Generates a table of contents for Markdown files.
- Supports both single Markdown files and directories containing multiple Markdown files.
- Option to search directories recursively for Markdown files.
- Simple and easy-to-use command-line interface.

## Installation

Requires python3 with venv. Simply run `BUILD.sh` and the executable should be generated in `./build`.

If you want to use it without a relative path, add it to your bin/PATH, or create an alias using an absolute path.

*Note*: I've only tested this on UNIX based systems (Linux, Mac). If you are running into problems feel free to submit an issue, or take inspiration from the `BUILD.sh` script. If you're on Windows you might need to change some of the commands to their PowerShell equivalents, or work out any quirks stemming from cross-platform python (though I hope this isn't an issue).

## Usage

```bash
toc [options] [files/directory]
```

### Example

You can follow along with the following repo

```bash
git clone git@github.com:elimelt/notes.git
```

```bash
# generate a markdown table of contents a single file
toc notes/distributed-systems/consistency.md

# a few files using wild card
toc notes/distributed-systems/*

# list of files
toc notes/distributed-systems/consistency.md notes/algorithms/DAGs.md

# many files recursively
toc -r notes

# create the table of contents for this file
toc -f md  -d 2 --no-path  ./README.md
```

### Reference

| Option | Description |
| --- | --- |
| `-r`, `--recursive` | Search directories recursively for markdown files |
| `-f`, `--format` | Output format for the table of contents (choices: `yaml`, `md`, `console`) |
| `-d`, `--depth` | Minimum heading level to include in the table of contents |
| `--no-path` | Don't print the file path |
