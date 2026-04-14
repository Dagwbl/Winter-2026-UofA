# AGENTS.md - Winter-2026 Course Repository

This is a Quarto-based academic course assignment repository for University of Alberta courses. It contains course assignments written in Quarto (markdown-based documents) with supporting Python utility scripts.

## Project Structure

```
Winter-2026/
├── .quarto/              # Quarto project configuration (generated)
├── .vscode/              # VS Code settings
├── _extensions/         # Quarto extensions
├── Assets/               # Static assets (images, etc.)
├── utils/                # Python utility scripts
│   ├── rename_assignment.py
│   ├── combine_ppts_to_pdf.py
│   └── setup_env.py
├── references.bib        # BibTeX references
├── README.md
└── [Course-Folders]/     # e.g., CIV-E-665, MIN-E-620, MIN-E-630
    └── Assignment-*/
```

## Build Commands

### Quarto

This is primarily a **Quarto project**. Render assignments with:

```bash
# Render all Quarto documents in a course folder
quarto render <course-folder>/

# Render a specific assignment
quarto render <course-folder>/Assignment-N/

# Preview locally (dev server)
quarto preview <course-folder>/
```

### Python Scripts

The utility scripts in `utils/` can be run directly with Python:

```bash
# Rename assignment output files
python utils/rename_assignment.py <path-to-pdf>

# Combine PowerPoint files to PDF (Windows only, requires PowerPoint)
python utils/combine_ppts_to_pdf.py <source_dir> <output_pdf>

# Setup environment (sets QUARTO_PYTHON)
python utils/setup_env.py
```

### Running a Single Test

**No formal test suite exists** in this repository. The Python scripts are utility functions, not tested modules.

If tests were to be added, use `pytest`:

```bash
# Run all tests
pytest

# Run a single test file
pytest tests/test_specific.py

# Run a single test function
pytest tests/test_specific.py::test_function_name

# Run tests matching a pattern
pytest -k "test_name_pattern"
```

## Code Style Guidelines

### Python (utils/)

Follow these conventions when editing or adding Python code:

#### Imports
- Standard library imports first
- Third-party imports second
- Local imports last
- Separate groups with blank lines
- Use absolute imports within the project

```python
# Good
import os
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from utils.helpers import some_function
```

#### Formatting
- **4 spaces** for indentation (no tabs)
- Line length: max 100 characters (soft limit at 120)
- Use **f-strings** for string formatting
- Use trailing commas in multi-line collections

#### Types
- Use **type hints** for function signatures
- Use `Path` from `pathlib` for file paths (not strings)
- Use `Optional[T]` instead of `T | None` for Python < 3.10 compatibility

```python
# Good
def process_file(input_path: Path, output_path: Optional[Path] = None) -> bool:
    ...
```

#### Naming Conventions
- **Functions/variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private functions**: prefix with underscore `_private_func`

#### Docstrings
Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Short description of what the function does.

    Longer description if needed.

    Args:
        param1: Description of first parameter.
        param2: Description of second parameter.

    Returns:
        True if successful, False otherwise.

    Raises:
        ValueError: If param2 is negative.
    """
```

#### Error Handling
- Use explicit exception types when possible
- Handle errors early with guard clauses
- Provide informative error messages
- Use `sys.exit(1)` for fatal errors in CLI scripts

```python
# Good
if not input_file.exists():
    print(f"Error: Input file not found: {input_file}")
    sys.exit(1)

try:
    result = risky_operation()
except SpecificError as e:
    print(f"Error during operation: {e}")
    return False
```

#### Section Comments
Use these separators for logical code sections:

```python
# ==============================================================================
# Section Name
# ==============================================================================
```

### Quarto Documents

When editing `.qmd` files:

- Use markdown headers (`#`, `##`, `###`) for hierarchy
- Use code blocks with language identifiers: ` ```python `
- Use `$...$` for inline math, `$$...$$` for display math
- Keep lines reasonably short for version control

### General

- **No trailing whitespace**
- **EOF newline** at end of files
- **No auto-generated comments** (e.g., "# Author:", "# Created:")
- Use meaningful variable/function names
- Keep functions focused and small (< 50 lines when possible)
- Comment *why*, not *what*

## Dependencies

Python dependencies are managed manually. Key dependencies used:

- `numpy`, `matplotlib` - Numerical computing and plotting
- `pywin32` - Windows PowerPoint automation
- `PyPDF2` - PDF manipulation
- `yaml` (PyYAML) - YAML parsing

For Quarto rendering, ensure Quarto is installed and `QUARTO_PYTHON` environment variable points to a Python with required packages.

## Working with This Repository

1. **Quarto rendering**: Use `quarto render` to generate PDFs from `.qmd` files
2. **Python utilities**: Run scripts from repository root with `python utils/script.py`
3. **Assets**: Place images in `Assets/` or course-specific folders
4. **References**: Add BibTeX entries to `references.bib`

## Notes for AI Agents

- This is primarily a **document authoring workflow**, not a software project
- Most files are Quarto markdown (`.qmd`) and rendered PDFs
- Python scripts are utility helpers, not core functionality
- No CI/CD pipeline exists
- No formal test framework is configured
