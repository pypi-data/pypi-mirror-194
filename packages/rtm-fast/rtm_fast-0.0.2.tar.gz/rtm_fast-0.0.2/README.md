# RTM FAST Package

This is a RTM FAST package.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install rtm-fast.

```bash
pip install rtm-fast==0.0.2
```

## Usage

```python
import rtm-fast

from rtm_fast_unification.ds.tool_objects.tool_selection import get_tool_object
```

## Contributing

Before updating the package, please run these command in Windows cmd.
```bash
py -m pip install --upgrade pip
py -m pip install --upgrade build
```
Now to Update the package, please follow these steps.

1. Please change the ds code and update the dependency array in pyproject.toml file if required.
2. Build the project in the directory where your pyproject.toml file is present using 
```bash
py -m build
```
3. Now to publish the package to PyPi please use the below command
```bash
py -m pip install --upgrade twine
py -m twine upload --repository testpypi dist/*
```
The upload command will ask for username and password. Provide it and your package will be published.
## License

[MIT](https://choosealicense.com/licenses/mit/)