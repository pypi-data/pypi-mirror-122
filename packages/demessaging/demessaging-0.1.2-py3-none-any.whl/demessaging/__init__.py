"""Main module to start a backend module from the command-line."""
from demessaging.backend import main, BackendModule  # noqa: F401
from demessaging.config import configure, registry


__all__ = ["main", "configure", "registry", "BackendModule"]

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
