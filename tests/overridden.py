"""Overrides."""
from pep562 import Pep562
import sys
import warnings

__version__ = (1, 0, 0)
__all__ = ("__version__",)
__deprecated__ = {
    "version": ("__version__", __version__)
}

PY37 = sys.version_info >= (3, 7)


def __getattr__(name):  # noqa: N807
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


def __dir__():  # noqa: N807
    """Module directory."""

    return sorted(list(__all__) + list(__deprecated__.keys()))


Pep562(__name__)
