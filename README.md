# brown

A Python formatter focused on consistent spacing and blank lines without altering code structure.

## Overview

Most formatters are overly aggressive, often refactoring logic or wrapping lines in ways that disrupt the original readability of the code. brown takes a different approach by focusing exclusively on horizontal and vertical whitespace.

It ensures proper spacing around operators and delimiters while maintaining consistent blank line intervals. brown does not wrap lines, move code blocks, or modify logic, ensuring your personal coding style remains intact while the formatting stays clean.

## Features

* **Whitespace Consistency**: Automatic handling of spaces around operators, brackets, and commas.
* **Vertical Rhythm**: Automatic management of blank lines between functions, classes, and imports.
* **Non-Destructive**: Does not perform line-wrapping or structural refactoring.
* **IDE Integration**: Syntax errors are reported with clickable file paths for immediate navigation in editors like VS Code or PyCharm.

## Installation

### From Source
Requires Python 3.10+.
```bash
pip install -r requirements.txt
python3 brown.py path/to/file.py
```

### Standalone Binary

If you don't want to manage a Python environment, download the latest pre-compiled executable from the Releases page.


## License

Distributed under the MIT License. See LICENSE for more information.