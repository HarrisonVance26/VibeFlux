# VibeFlux/utils/Sysinfo.py
"""
VibeFlux System Information Utilities.

This module provides lightweight helpers to query runtime environment details
and print a single standardized startup banner.

Primary goals:
- Correctly identify Windows 10 vs Windows 11 by using registry/build info.
- Offer a unified `get_runtime_info()` dictionary for logging/diagnostics.
- Avoid repeated banner printing during multiple imports (common in Python packages).

Public API
----------
- get_os_pretty() -> str
- get_runtime_info() -> dict
- print_banner(pkg_name: str, version: str, verbose: bool = True) -> None
"""

from __future__ import annotations

import os
import sys
import platform
from typing import Dict, Any


def get_os_pretty() -> str:
    """
    Return a human-friendly operating system string.

    On Windows, this function tries to read OS marketing name and version
    from the registry (e.g., "Windows 11 Pro 23H2 (build 22631.3007)").
    This is more accurate than `platform.release()`, which often returns "10"
    even on Windows 11.

    On non-Windows platforms, it returns a concise string like
    "<system> <release>" derived from `platform.uname()`.

    Returns
    -------
    str
        A human-friendly OS description.

    Examples
    --------
    - "Windows 11 Pro 23H2 (build 22631.3007)"
    - "Windows 10 (build 19045)"
    - "Linux 6.5.0-14-generic"
    - "Darwin 23.1.0"
    """
    if sys.platform.startswith("win"):
        try:
            import winreg  # type: ignore

            key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as k:
                # Examples:
                # ProductName: "Windows 11 Pro"
                # DisplayVersion: "23H2"
                # CurrentBuildNumber: "22631"
                # UBR: 3007
                product = winreg.QueryValueEx(k, "ProductName")[0]
                display = winreg.QueryValueEx(k, "DisplayVersion")[0]
                build = winreg.QueryValueEx(k, "CurrentBuildNumber")[0]
                ubr = winreg.QueryValueEx(k, "UBR")[0]
            return f"{product} {display} (build {build}.{ubr})"
        except Exception:
            # Fallback: build number heuristic
            # Windows 11 starts around build 22000+
            win = sys.getwindowsversion()
            build = getattr(win, "build", 0)
            name = "Windows 11" if build >= 22000 else "Windows 10"
            return f"{name} (build {build})"

    u = platform.uname()
    return f"{u.system} {u.release}"


def get_runtime_info() -> Dict[str, Any]:
    """
    Collect runtime environment information for logging/diagnostics.

    This function returns a dictionary with basic system information and
    optionally adds versions of key libraries when available.

    Keys included by default
    ------------------------
    python : str
        Python version in "major.minor.micro" format.
    os : str
        Pretty OS string from `get_os_pretty()`.
    arch : str
        Machine architecture (e.g., "AMD64", "x86_64", "arm64").
    hostname : str
        Hostname of the current machine.
    cpu_count : int
        Number of logical CPUs (or 0 if unknown).

    Optional keys (only present if import succeeds)
    -----------------------------------------------
    pyside6 : str
        PySide6 version.
    qt : str
        Qt runtime version.
    opencv : str
        OpenCV version.

    Returns
    -------
    Dict[str, Any]
        Runtime information dictionary.

    Examples
    --------
    >>> info = get_runtime_info()
    >>> info["python"]
    '3.10.16'
    >>> info["os"]
    'Windows 11 Pro 23H2 (build 22631.3007)'
    """
    info: Dict[str, Any] = {}
    info["python"] = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    info["os"] = get_os_pretty()
    info["arch"] = platform.machine()
    info["hostname"] = platform.node()
    info["cpu_count"] = os.cpu_count() or 0

    # Optional: Qt/PySide6 versions
    try:
        from PySide6.QtCore import __version__ as pyside_ver, qVersion  # type: ignore

        info["pyside6"] = pyside_ver
        info["qt"] = qVersion()
    except Exception:
        pass

    # Optional: OpenCV version
    try:
        import cv2  # type: ignore

        info["opencv"] = cv2.__version__
    except Exception:
        pass

    return info


def print_banner(pkg_name: str, version: str, verbose: bool = True) -> None:
    """
    Print a standardized one-time banner for VibeFlux.

    The banner format is:
        "<pkg_name> <version> Python-<pyver> (<os_pretty>)"

    This function uses a guard attribute on the `sys` module to ensure the
    banner is printed only once per Python process:
        sys._vibeflux_banner_printed = True

    Parameters
    ----------
    pkg_name : str
        Package name to display (e.g., "VibeFlux").
    version : str
        Package version to display (e.g., "0.7.1").
    verbose : bool, optional
        If False, the function returns immediately and prints nothing.
        Default is True.

    Returns
    -------
    None
        This function prints to stdout and returns None.

    Notes
    -----
    - If you want to reset the guard (generally not recommended), you can do:
        delattr(sys, "_vibeflux_banner_printed")
      or:
        sys._vibeflux_banner_printed = False

    Examples
    --------
    >>> print_banner("VibeFlux", "0.7.1")
    VibeFlux 0.7.1 Python-3.10.16 (Windows 11 Pro 23H2 (build 22631.3007))
    """
    if not verbose:
        return

    # Prevent repeated printing across multiple imports/classes
    if getattr(sys, "_vibeflux_banner_printed", False):
        return
    sys._vibeflux_banner_printed = True

    info = get_runtime_info()
    py = f"Python-{info.get('python', 'unknown')}"
    os_str = info.get("os", "unknown OS")
    print(f"{pkg_name} {version} {py} ({os_str})")
