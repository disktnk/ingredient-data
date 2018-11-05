# Ingredient data

Collect ingredient and count up each

## Install

### Windows binary

Download latest `ingred-data.exe` file from [release](https://github.com/disktnk/ingredient-data/releases) page.

### From source

```bash
$ git clone https://github.com/disktnk/ingredient-data.git
$ cd ingredient-data
$ pip install -e .
```

enable to run `ingred-data` binary.

## Prepare data

*data.txt*

```
[Title]
Components list
...

[Title]
Components list
...
```

- word separator: `,`, `、`, `，`
- commodity separator: more than one blank line

## Run

### Output Excel file

```bash
$ ingred-data excel

$ # or
$ ingred-data
```

`excel` sub-command will make "summary.xlsx" file, written result of counting up in "count" sheet, and list of products in "master" sheet. No sub-command is same as `excel` mode.

- `--out`, `-o`: output file name, "summary.xlsx" is set on default.

### Show on console

```bash
$ ingred-data -n 20 count
$ # show result of top 20 counting up
```

```bash
$ ingred-data list i
$ # show all ingredients

$ ingred-data list p
$ # show all products
```

- `--num`, `-n`: number of how many to show, both `count` and `list` sub-command support. `-1` is set on default.
- `--id`, `-i`: number of ID to show, `list` sub-command supports.

## For develop

### Make executable file (Windows)

use [PyInstaller](https://www.pyinstaller.org/) (`pip install pyinstaller`)

```bash
$ pyinstaller src\show.py --name ingred-data -F
```

`ingred-data.exe` will created at `dist` directory.
