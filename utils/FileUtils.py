# VibeFlux, AGPL-3.0 license
import os
import yaml
from typing import Any, Dict, Optional


def readQssFile(qss_file_path, encoding='utf-8'):
    """
    Read and return the content of a QSS file using the specified encoding.

    Args:
        qss_file_path (str): The path to the QSS file.
        encoding (str): The encoding used to read the file. Defaults to 'utf-8'.

    Returns:
        str: The content of the QSS file.

    Raises:
        FileNotFoundError: If the QSS file does not exist.
        IOError: If there is an error reading the file.
        UnicodeDecodeError: If decoding the file fails.
    """
    try:
        with open(qss_file_path, 'r', encoding=encoding) as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {qss_file_path}")
    except IOError as e:
        raise IOError(f"Error reading file {qss_file_path}: {e}")
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"Error decoding file {qss_file_path} with encoding {encoding}: {e}")


def _extract_leaf_keys(nested_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively traverse a nested dictionary and map each leaf key to its value
    by using only the final key name. If a duplicate key is found, keep the first
    and print a warning.

    Example:
        If the YAML structure is:

            database:
              db_file: "UserDatabase.db"
            paths:
              db_file: "OtherDatabase.db"   # Duplicate key
              qss_file: "main_text_black.qss"

        We will keep:
            "db_file" -> "UserDatabase.db"
            "qss_file" -> "main_text_black.qss"

        and print a warning about "db_file" being duplicated.

    Args:
        nested_dict (Dict[str, Any]): Nested configuration dictionary.

    Returns:
        Dict[str, Any]: A new dictionary with only leaf key names (no nesting).
    """
    result: Dict[str, Any] = {}

    def _traverse(current: Dict[str, Any]) -> None:
        for key, value in current.items():
            if isinstance(value, dict):
                # Recurse if the value is another dictionary
                _traverse(value)
            else:
                # Leaf key found
                if key in result:
                    print(f"Warning: Duplicate key '{key}' found. "
                          f"Existing value '{result[key]}' is kept; new value '{value}' is ignored.")
                else:
                    result[key] = value

    _traverse(nested_dict)
    return result


class QConfig:
    """
    A class for loading a YAML configuration file and extracting
    only the final (leaf) keys for direct access.

    Usage Example:
    --------------
    1) Create an instance of Config:
       >>> config = QConfig("path/to/your.yaml")

    2) Access values by leaf key:
       >>> db_file = config["db_file"]
       >>> print(db_file)

    3) If the key does not exist, it returns None by default:
       >>> some_val = config["non_existent_key"]
       >>> print(some_val)   # None

    4) Safely get values with a default:
       >>> some_val = config.get("non_existent_key", default="my_default")
       >>> print(some_val)   # "my_default"
    """

    def __init__(self, file_path: str) -> None:
        """
        Constructor that loads the YAML file, extracts leaf keys, and stores them
        in a single-level dictionary. If the file does not exist or cannot be parsed,
        an empty dictionary is used.

        Args:
            file_path (str): The path to the YAML configuration file.
        """
        self._data: Dict[str, Any] = {}
        self._load_config_yaml(file_path)

    def _load_config_yaml(self, file_path: str) -> None:
        """
        Internal method to load and parse the YAML file, then extract only leaf keys.

        Args:
            file_path (str): The path to the YAML configuration file.
        """
        if not os.path.isfile(file_path):
            print(f"Warning: File not found or not a valid file: {file_path}")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if not data:
                    print(f"Warning: YAML file is empty or parsed as None: {file_path}")
                    return
                # Extract only the leaf keys
                self._data = _extract_leaf_keys(data)
        except yaml.YAMLError as e:
            print(f"Error: YAML parsing error: {e}")
        except Exception as e:
            print(f"Error: Failed to read file. Details: {e}")

    def __getitem__(self, key: str) -> Any:
        """
        Enables dict-like access: config[key].

        Args:
            key (str): The leaf key to retrieve.

        Returns:
            Any: The stored value, or None if key does not exist.
        """
        return self._data.get(key, None)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Returns the value for the specified key, or a default if key is not found.

        Args:
            key (str): The leaf key to retrieve.
            default (Any): The default value if the key is missing.

        Returns:
            Any: The retrieved value or the `default` if key not found.
        """
        return self._data.get(key, default)

    def keys(self) -> Any:
        """
        Lists the keys that have been extracted from the YAML file.

        Returns:
            Any: The collection of leaf keys.
        """
        return self._data.keys()

    def as_dict(self) -> Dict[str, Any]:
        """
        Returns a shallow copy of the internal dictionary for direct manipulation.

        Returns:
            Dict[str, Any]: A copy of the flattened data with only leaf keys.
        """
        return dict(self._data)
