# Ingredient data

Collect ingredient and count up each

## Install

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

```bash
$ ingred-data -n 20 count
```

```bash
$ ingred-data list i
$ # show ingredients

$ ingred-data list p
$ # show products
```

## Make executable file (Windows)

use [PyInstaller](https://www.pyinstaller.org/) (`pip install pyinstaller`)

```bash
$ pyinstaller src\show.py --name ingred-data -F
```

`ingred-data.exe` will created at `dist` directory.
