# VibeFlux/_runtime.py
from __future__ import annotations

import warnings
from importlib.metadata import PackageNotFoundError, version

_REQUIRED_MIN = {
    "numpy": None,
    "opencv-python": "4.5.5.64",
    "Pillow": "9.0.1",
    "PySide6": "6.4.2",
    "PyYAML": "6.0",
    "captcha": "0.4",
    "aggdraw": "1.3.19",
    "ruamel.yaml": "0.18.6",
}


def _tuple_ver(v: str) -> tuple[int, ...]:
    parts = []
    for x in v.replace("-", ".").split("."):
        if x.isdigit():
            parts.append(int(x))
        else:
            break
    return tuple(parts)


def check_dependencies() -> None:
    for pkg, min_ver in _REQUIRED_MIN.items():
        try:
            actual = version(pkg)
        except PackageNotFoundError:
            warnings.warn(f"[VibeFlux] Missing dependency: {pkg}", RuntimeWarning, stacklevel=2)
            continue

        if min_ver:
            if _tuple_ver(actual) < _tuple_ver(min_ver):
                warnings.warn(
                    f"[VibeFlux] {pkg}>={min_ver} recommended, but {actual} is installed.",
                    RuntimeWarning,
                    stacklevel=2,
                )
