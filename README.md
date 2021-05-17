[![Donate via PayPal][donate-image]][donate-link]
[![Discord][discord-image]][discord-link]
[![Build][github-ci-image]][github-ci-link]
[![Coverage Status][codecov-image]][codecov-link]
[![PyPI Version][pypi-image]][pypi-link]
[![PyPI - Python Version][python-image]][pypi-link]
![License][license-image-mit]

# PEP 562

## Overview

A backport of PEP 562. Allows controlling a module's `__dir__` and `__getattr__`. Useful for deprecating attributes.
Works for Python 2.7+. And while it works on Python 3.7, it is recommended to use the official Python 3.7 implementation
where applicable.

This module can be installed and used as a dependency, or if desired, it is easy to vendor as the license is quite
permissible, and the code is contained in a single file.

Once Python 3.6 is end of life, this module will be irrelevant and will no longer receive active support.

## Install

Installation is done with `pip`:

```
pip install pep562
```

## Vendoring

Simply copy the file `pep562/__init__.py` to your project and rename to `pep562`.  Import and use as needed.

## Usage

Here is a simple example where we deprecate the attribute `version` for the more standardized `__version__`.

```py
from pep562 import pep562
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


pep562(__name__)
```

## License

MIT License

Copyright (c) 2018 - 2021 Isaac Muse <isaacmuse@gmail.com>

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

[github-ci-image]: https://github.com/facelessuser/pep562/workflows/build/badge.svg?branch=master&event=push
[github-ci-link]: https://github.com/facelessuser/pep562/actions?query=workflow%3Abuild+branch%3Amaster
[discord-image]: https://img.shields.io/discord/678289859768745989?logo=discord&logoColor=aaaaaa&color=mediumpurple&labelColor=333333
[discord-link]:https://discord.gg/TWs8Tgr
[codecov-image]: https://img.shields.io/codecov/c/github/facelessuser/pep562/master.svg?logo=codecov&logoColor=aaaaaa&labelColor=333333
[codecov-link]: https://codecov.io/github/facelessuser/pep562
[pypi-image]: https://img.shields.io/pypi/v/pep562.svg?logo=pypi&logoColor=aaaaaa&labelColor=333333
[pypi-link]: https://pypi.python.org/pypi/pep562
[python-image]: https://img.shields.io/pypi/pyversions/pep562?logo=python&logoColor=aaaaaa&labelColor=333333
[license-image-mit]: https://img.shields.io/badge/license-MIT-blue.svg?labelColor=333333
[donate-image]: https://img.shields.io/badge/Donate-PayPal-3fabd1?logo=paypal
[donate-link]: https://www.paypal.me/facelessuser
