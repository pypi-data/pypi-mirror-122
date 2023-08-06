"""Integration between j5 and zoloto."""
from .backends import ZolotoSingleHardwareBackend
from .board import ZolotoCameraBoard

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "ZolotoCameraBoard",
    "ZolotoSingleHardwareBackend",
]
