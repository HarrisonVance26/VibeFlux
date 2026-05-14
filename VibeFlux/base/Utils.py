import inspect
import os
from typing import Optional


def pathExists(path: str) -> bool:
    """
    Checks if the specified path exists.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path exists, False otherwise.
    """
    return os.path.exists(path)


def catchPath(relative_path: str, base_path: Optional[str] = None, path_type: Optional[str] = "current") -> str:
    """
    Appends an absolute path prefix to a single relative path.

    Args:
        relative_path (str): The relative path string.
        base_path (Optional[str]): The base path. If None, the path is determined based on path_type.
        path_type (Optional[str]): The type of base path to use.
                                   "current" for the caller's file directory,
                                   "project" for the project's root directory,
                                   or "parent" for the parent directory of the caller's file.

    Returns:
        str: The combined absolute path.

    Raises:
        ValueError: If the provided path is invalid.
    """
    if base_path is None:
        # Get the file path of the caller
        caller_frame = inspect.stack()[1]
        caller_path = caller_frame.filename
        caller_dir = os.path.dirname(os.path.abspath(caller_path))

        if path_type == "current":
            base_path = caller_dir
        elif path_type == "project":
            # Assuming the project directory is the first directory without __init__.py
            while os.path.exists(os.path.join(caller_dir, '../__init__.py')):
                caller_dir = os.path.dirname(caller_dir)
            base_path = caller_dir
        elif path_type == "parent":
            base_path = os.path.dirname(caller_dir)
        else:
            raise ValueError(f"Invalid path_type '{path_type}'. Expected 'current', 'project', or 'parent'.")

    # Normalize the relative path
    cleaned_relative_path = os.path.normpath(relative_path.lstrip('/\\')) if os.name == 'nt' else relative_path

    # Join the base path with the relative path
    absolute_path = os.path.join(base_path, cleaned_relative_path)

    # Normalize the path
    absolute_path = os.path.normpath(absolute_path)

    return absolute_path
