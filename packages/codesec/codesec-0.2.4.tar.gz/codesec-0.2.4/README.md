# codesec

## Installation
```
$ pip install codesec
```
### Dependencies
Python dependencies included during pip install:
- `pyperclip`

No other dependencies on Windows and Mac OS.

Other systems may need to install `xclip` or `xsel` packages

## Usage
``` 
usage: codesec [-h] [-s] [--symbols] [--reset] [title]

Create pretty printed section title for your code

positional arguments:
  title        title of your section

optional arguments:
  -h, --help   show this help message and exit
  -s , --set   configure settings: length, outer_corners, inner_corners,
               outer_edges, inner_edges, center_fill, comment
  --symbols    prints out common ascii symbols for decoration
  --reset      reset config
```

### Example:

```bash
$ codesec --set delimiter
Default delimiter: "# h "
Current delimiter: "# h "
Enter setting: "# !h "
$ codesec src tests example.py
Found 4 files
Editing src/app.py
Editing src/utils.py
Editing tests/test_func.py
Editing example.py
```
Before:
```python
# app.py

# !h Boring Functions

def bar():
    pass

# !h Cool Functions

def foo():
    print("Somthing cool")

def main():
    foo()

```

After:

```python
# app.py

# +------------╔══════════════════╗------------+ #
# |::::::::::::║ Boring Functions ║::::::::::::| #
# +------------╚══════════════════╝------------+ #

def bar():
    pass

# +-------------╔════════════════╗-------------+ #
# |:::::::::::::║ Cool Functions ║:::::::::::::| #
# +-------------╚════════════════╝-------------+ #

def foo():
    print("Somthing cool")

def main():
    foo()

```

Generate and copy individual sections
```bash
$ codesec --set length

Default length: 80
Current length: 80
Enter setting: 50
Preview:
# +--------------╔===============╗-------------+ #
# |::::::::::::::║ Section Title ║:::::::::::::| #
# +--------------╚===============╝-------------+ #

$ codesec --set inner_edges

Default inner_edges: =,=,║,║
Current inner_edges: =,=,║,║
Enter setting: ≡+,≡+,►,◄
Preview:
# +--------------╔≡+≡+≡+≡+≡+≡+≡+≡╗-------------+ #
# |::::::::::::::► Section Title ◄:::::::::::::| #
# +--------------╚≡+≡+≡+≡+≡+≡+≡+≡╝-------------+ #

$ codesec -t "My Section"

Copied:
# +---------------╔≡+≡+≡+≡+≡+≡+╗---------------+ #
# |:::::::::::::::► My Section ◄:::::::::::::::| #
# +---------------╚≡+≡+≡+≡+≡+≡+╝---------------+ #
```