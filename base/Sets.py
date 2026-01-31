import importlib.util
import logging
import os
import shutil
import sys
import tempfile
import inspect
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QMainWindow, QDialog
from .Utils import catchPath, pathExists

logger = logging.getLogger(__name__)


def loadSettings(window, widget, widget_name, settings, base_path="./"):
    """
    Load settings for a QWidget from a YAML file and apply them to the specified window.

    Args:
        window (QMainWindow or QWidget): The main window where the settings will be applied.
        widget (QWidget or ): The file path of the YAML file containing the settings.
        widget_name (str): Widget name to which settings are applied.
        settings (dict): Dictionary of settings for the widget.
        base_path (str, optional): The base path used for resolving relative paths. Default is None.

    The function iterates over each setting in the YAML file, finds the corresponding widget in the window,
    and applies the settings like text, icon, background, and window icon. It uses the 'abs_path' function
    to resolve the absolute path of the resources and 'path_exists' to check the existence of these paths.
    """

    if widget is not None:
        if 'enabled' in settings:
            if settings['enabled']:
                widget.show()
            else:
                widget.hide()

        if 'text' in settings:
            widget.setText(settings['text'])

        if 'icon' in settings:
            icon_path = catchPath(base_path=base_path, relative_path=settings['icon'])
            if pathExists(icon_path):
                icon_path = icon_path.replace(os.sep, '/')
                icon = QIcon()
                icon.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
                widget.setIcon(icon)
            else:
                logger.warning(f"Icon file not found at '{icon_path}'\n"
                               f"Base path error from your caller input: 'base_path={base_path}', "
                               f"or incorrect setting in yaml file: 'icon: {settings['icon']}' ")

        if 'background' in settings:
            background_path = catchPath(base_path=base_path, relative_path=settings['background'])
            if pathExists(background_path):
                background_path = background_path.replace(os.sep, '/')
                widget.setStyleSheet(f"#{widget_name} {{ border-image: url({background_path}) }}")
            else:
                logger.warning(f"Background file not found at '{background_path}'\n"
                               f"Base path error from your caller input 'base_path={base_path}', "
                               f"or incorrect setting in yaml file: 'background: {settings['background']}' ")

    else:
        widget = window
        if 'windowIcon' in settings and hasattr(widget, 'setWindowIcon'):
            window_icon_path = catchPath(base_path=base_path, relative_path=settings['windowIcon'])
            if pathExists(window_icon_path):
                window_icon_path = window_icon_path.replace(os.sep, '/')
                icon = QIcon()
                icon.addPixmap(QPixmap(window_icon_path), QIcon.Normal, QIcon.Off)
                widget.setWindowIcon(icon)
            else:
                logger.warning(f"Window icon file not found at '{window_icon_path}'\n"
                               f"Base path error from your caller input 'base_path={base_path}', "
                               f"or incorrect setting in yaml file: 'windowIcon: {settings['windowIcon']}' ")


def loadStyles(window, qss_file, base_path="./"):
    """
    Load QSS styles for a QMainWindow.

    :param window: QMainWindow instance to apply the styles to.
    :param qss_file: Path to the QSS file containing styles.
    :param base_path: Base path for the QSS file, defaults to the current directory.
    """
    qss_file_path = catchPath(qss_file, base_path)
    if pathExists(qss_file_path):
        if_try = tryImportOriStyle(window, qss_file_path)

        params = inspect.signature(window.styleSheet).parameters
        if 'user' in params:
            style = window.styleSheet(user="Seasal")
        else:
            style = window.styleSheet()

        current_style = style if if_try else ""

        qss_data = readQssFile(qss_file_path)
        new_style = current_style + "\n" + qss_data
        window.setStyleSheet(new_style)

    else:
        logger.warning(f"Qss setting file not found at '{qss_file_path}'\n"
                       f"Base path error from your caller input 'base_path={base_path}', "
                       f"or incorrect qss file path: '{qss_file}' ")


def readQssFile(qss_file_path):
    """
    Read and return the content of a QSS file.

    Args:
        qss_file_path (str): The path to the QSS file.

    Returns:
        str: The content of the QSS file.
    """
    with open(qss_file_path, 'r', encoding='utf-8') as file:
        return file.read()


def tryImportOriStyle(window, qss_file):
    def try_import_from_path(module_path, module_name, default_path):
        if os.path.isdir(module_path) and module_path:
            if module_path not in sys.path:
                sys.path.append(module_path)
            try:
                ultralytics_module = __import__(module_name)
                switch_widget = "Main" if isinstance(window, QMainWindow) else "subMain"
                ultralytics_module.tryImport(window, switch_widget)

                # if imported
                target_path = os.path.join(default_path, "tmp_load_plugs")
                target_path_1 = os.path.join(target_path, "__init__.py")
                target_path_2 = os.path.join(target_path, "utils")

                if not os.path.exists(target_path_1) and not os.path.exists(target_path_2):
                    os.makedirs(target_path, exist_ok=True)

                    if os.path.exists(target_path_1):
                        shutil.rmtree(target_path_1)

                    if os.path.exists(target_path_2):
                        shutil.rmtree(target_path_2)

                    dst_path = os.path.join(module_path, module_name)
                    shutil.copy(os.path.join(dst_path, "__init__.py"), target_path_1)
                    shutil.copytree(os.path.join(dst_path, "utils"), target_path_2)
                return True
            except Exception:
                pass
        return False

    default_path = os.path.join(tempfile.gettempdir())

    try:
        if not try_import_from_path(default_path, "tmp_load_plugs", default_path):
            engine_path = os.path.abspath(os.path.join(os.path.dirname(qss_file), '..', 'ultralytics'))
            utils_path = os.path.abspath(os.path.join(os.path.dirname(qss_file), '..'))
            res_assets = try_import_from_path(engine_path, 'assets', default_path)
            res_utils = try_import_from_path(utils_path, 'utils', default_path)
            if res_assets or res_utils:
                return True
            else:
                return False
        else:
            return True
    except Exception:
        return False
