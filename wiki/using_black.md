## Useful:
If a block cannot be formatted (for example, due to compatibility reasons), add a comment:
```
# fmt: off
non_formatted_code = {
    "key": "value",
    "data": [1, 2, 3,]
}
# fmt: on
```
- \# fmt: off — before the code that should not be formatted.

- \# fmt: on — after this code, to enable auto-formatting again.

## Links:
- The Black documentation: https://black.readthedocs.io
- Config examples: https://github.com/pre-commit/pre-commit-hooks