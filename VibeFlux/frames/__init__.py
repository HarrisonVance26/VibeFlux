# VibeFlux, AGPL-3.0 license
"""Compatibility aliases for the historical VibeFlux.frames import path."""

from ..widgets import *  # noqa: F401,F403
from ..widgets import __all__ as _widgets_all

__all__ = tuple(_widgets_all)
