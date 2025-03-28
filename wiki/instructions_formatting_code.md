## Setting up a pre-commit hook for formatting code using Black

- The black configuration settings are located in .pre-commit-config.yaml

- After cloning the project, run the `pre-commit install` command once in the virtual environment. Next, the hook will be triggered with each commit.

- If black finds a problem in the code, he will fix it and you need to commit again.

- You can check for a hook with `cat command.git/hooks/pre-commit` if it returns the code then the hook is installed.

### Useful:
If a block cannot be formatted (for example, due to compatibility reasons), add a comment:
```
# fmt: off
non_formatted_code = {
    "key": "value",
    "data": [1, 2, 3,]
}
# fmt: on
```

- The Black documentation: https://black.readthedocs.io
- Config examples: https://github.com/pre-commit/pre-commit-hooks