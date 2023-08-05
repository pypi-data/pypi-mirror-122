# Omniblack Setup

Omniblack Setup is a library that gives setuptools [PEP 621] compatibility.

At the moment omniblack.setup does not support all of [PEP 621]
in particular when there is a string or table option this library only
supports the table option right now.

## Usage

To use this library call `omniblack.setup:setup` in `setup.py`.

```python
from omniblack.setup import setup

setup()
```


[PEP 621]:  https://www.python.org/dev/peps/pep-0621/
