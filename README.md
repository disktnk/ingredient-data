# Ingredient data

Collect ingredient and count up each

## Setup module

```bash
$ git clone https://github.com/disktnk/ingredient-data.git
$ cd ingredient-data
$ pip install texttable zenhan
```

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
$ python show.py -n 20 count
```

```bash
$ python show.py list i
$ # show ingredients

$ python show.py list p
$ # show products
```
