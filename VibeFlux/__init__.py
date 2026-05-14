# VibeFlux, AGPL-3.0 license
# File: __init__.py | Updated: 2026-05-13
"""
VibeFlux is a Python library created by Harrison Vance for
the convenient creation of PySide6 applications that interact with deep learning models.
It provides user interface management and beautification, database management,
image/video/camera processing, model interface definition, LLM API calling, and event handling.
This makes it easy for users to create deep learning applications.

Python Version Required: 3.7+
Dependencies: numpy, opencv-python>=4.5.5.64, Pillow>=9.0.1, PySide6>=6.4.2, PyYAML>=6.0, captcha>=0.4
"""
import sys
import os
from PIL import ImageFont
import warnings
from . import RecSystem
from .llms import APIKeyManager, LLMClient, ModelRegistry

# Check Python version
if not sys.version_info >= (3, 7):
    warnings.warn("Python 3.7 or above is recommended.")

# Check other dependencies
required_packages = {
    "numpy": "",  # no specific version requirement
    "opencv-python": "4.5.5.64",
    "Pillow": "9.0.1",
    "PySide6": "6.4.2",
    "PyYAML": "6.0",
    "captcha": "0.4",
    "aggdraw": "1.3.19",
    "ruamel.yaml": "0.18.6",
}


if os.environ.get("VIBEFLUX_CHECK_DEPS") == "1":
    from ._runtime import check_dependencies
    check_dependencies()

# Get current script path
current_dir = os.path.dirname(os.path.realpath(__file__))

# Use os.path.join to join paths
font_path = os.path.join(current_dir, 'GB2312.ttf')

try:
    fontC = ImageFont.truetype(font_path, 24)  # Set display font
    fontB = ImageFont.truetype(font_path, 18)
except IOError:
    # Fall back to Pillow's default font when packaged font assets are unavailable.
    fontC = ImageFont.load_default()
    fontB = ImageFont.load_default()

__package_name__ = 'VibeFlux'
__version__ = '0.8.0'
__author__ = 'Harrison Vance'
__email__ = 'seasalwesley@gmail.com'
__license__ = 'AGPL-3.0-or-later'
__url__ = 'https://github.com/HarrisonVance26/VibeFlux'

VERBOSE = os.environ.get("VIBEFLUX_VERBOSE", "0") == "1"

try:
    if VERBOSE:
        from .utils.Sysinfo import print_banner
        print_banner(__package_name__, __version__, verbose=VERBOSE)
except Exception as e:
    warnings.warn(f"VibeFlux banner could not be printed: {e}")
