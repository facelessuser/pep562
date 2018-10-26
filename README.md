# PEP 562

## Overview

A backport of PEP 562. Allows controlling a module's `__dir__` and `__getattr__`. Useful for deprecating attributes. Works for Python 2.7+, and on versions greater than Python 3.7 it will do nothing allowing it to be used in projects that support Python 3.7 and below.

## Usage

Here is a simple example where we deprecate the attribute `version` for the more standardized `__version__`.

```py
from pep562 import Pep562
import sys
import warnings

__version__ = (1, 0, 0)
__all__ = ("__version__",)
__deprecated__ = {
    "version": ("__version__", __version__)
}

PY37 = sys.version_info >= (3, 7)


def __getattr__(name):
    """Get attribute."""

    deprecated = __deprecated__.get(name)
    if deprecated:
        stacklevel = 3 if PY37 else 4
        warnings.warn(
            "'{}' is deprecated. Use '{}' instead.".format(name, deprecated[0]),
            category=DeprecationWarning,
            stacklevel=stacklevel
        )
        return deprecated[1]
    raise AttributeError("module '{}' has no attribute '{}'".format(__name__, name))


def __dir__():
    """Module directory."""

    return sorted(list(__all__) + list(__deprecated__.keys()))


Pep562(__name__)
```

## License

MIT License

Copyright (c) 2018 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
