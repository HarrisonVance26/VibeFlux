# VibeFlux, AGPL-3.0 license
"""
VibeFlux is a Python library created by Harrison Vance for
the convenient creation of PySide6 applications that interact with deep learning models.
It provides user interface management and beautification, database management,
image/video/camera processing, model interface definition, and event handling.
This makes it easy for users to create deep learning applications.

Python Version Required: 3.7+
Dependencies: numpy, opencv-python>=4.5.5.64, Pillow>=9.0.1, PySide6>=6.4.2, PyYAML>=6.0, captcha>=0.4
"""
import sys
import os
import tempfile
from PIL import ImageFont
from PySide6.QtCore import QFile, QIODevice
import warnings
from . import RecSystem

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
    # If loading font from file system fails, try to load font from Qt resource system
    qfile = QFile(":/GB2312.ttf")
    qfile.open(QIODevice.ReadOnly)
    data = qfile.readAll().data()  # Get byte data

    try:
        # Create a temporary file
        temp_path = os.path.join(tempfile.gettempdir(), "temp_font.ttf")

        # Write font data into temporary file
        with open(temp_path, "wb") as f:
            f.write(data)
    except Exception as e:
        raise IOError("Unable to write font to temporary file: " + str(e))

    try:
        # Use Pillow to read font from temporary file
        fontC = ImageFont.truetype(temp_path, 24)
        fontB = ImageFont.truetype(temp_path, 18)
    except Exception as e:
        raise IOError("Unable to load font from temporary file: " + str(e))

__package_name__ = 'VibeFlux'
__version__ = '0.7.1'
__author__ = 'Harrison Vance'
__email__ = ''
__license__ = 'AGPL-3.0'
__url__ = 'https://github.com/HarrisonVance26/VibeFlux'

VERBOSE = True

try:
    # If QTFUSION_VERBOSE is True, print the information
    if VERBOSE:
        from .utils.Sysinfo import print_banner
        VERBOSE = True  # or QF_Config.VERBOSE if you prefer
        print_banner(__package_name__, __version__, verbose=VERBOSE)
except Exception as e:
    print(f"Exception occurred: {e}")
