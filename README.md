# Claudius

A terminal-based UI for managing `.claudeignore` files.

## Overview

Claudius is a command-line tool that provides a visual interface for managing `.claudeignore` files. It allows you to easily specify which files and directories should be excluded when sharing content with Claude AI. As projects grow in size, eventually you can't fit the entire codebase into the context window. This helps you easily manage which files get included

The app scans your file system recursively from the current working directory and displays files in a tree structure, making it easy to see which files are included in your `.claudeignore` file and to add or remove entries quickly.

## Installation

```bash
pip install claudius
```

Or install from source:

```bash
git clone https://github.com/yourusername/claudius.git
cd claudius
pip install -e .
```

## Usage

Navigate to your project directory and run:

```bash
claudius
```

This will launch the terminal UI and automatically load any existing `.claudeignore` file in the current directory.

## Features

- Visual representation of your file system as a tree
- Highlighting of files/folders currently included in `.claudeignore`
- Recursively include/exclude folders and their contents
- Keyboard-driven interface
- Persistent expansion state between sessions
- Live feedback when writing changes to the `.claudeignore` file

## Key Commands

| Key      | Action                               | Description                                               |
|----------|--------------------------------------|-----------------------------------------------------------|
| `j`      | Move Down                            | Move selection cursor down one item                       |
| `k`      | Move Up                              | Move selection cursor up one item                         |
| `f`      | Toggle Folder                        | Expand or collapse the selected folder                    |
| `i`      | Toggle Include                       | Include/exclude the selected item in `.claudeignore`      |
| `w`      | Write .claudeignore                  | Save current selections to the `.claudeignore` file       |
| `o`      | Expand All                           | Expand all folders in the file tree                       |
| `p`      | Collapse All                         | Collapse all folders in the file tree                     |
| `q`      | Quit                                 | Exit the application                                      |

## How It Works

Claudius uses a functional programming approach with clear separation between:

- **State management**: Tracks which files are included, folder expansion status, and selection
- **Actions**: Functions that have side effects (reading files, updating UI)
- **Calculations**: Pure functions for filtering and transforming data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT

## Credits

Claudius is built with [Textual](https://github.com/Textualize/textual), a TUI (Text User Interface) framework for Python.
