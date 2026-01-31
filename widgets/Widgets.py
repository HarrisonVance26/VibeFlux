# VibeFlux, AGPL-3.0 license
from typing import Optional, Tuple
import os
from concurrent.futures import ThreadPoolExecutor
from ..base.Manager import BaseDB

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import (QWidget, QPushButton)
from .BaseFrame import FBaseWindow, dispImage, FLoginDialog
from .ExtWidgets import *
from .SettingsDialog import SettingsDialog, ConfigDialog
from .TipsWidgets import MultiTipWidget
from ..styles import loadQssStyles, loadYamlSettings, BaseStyle


class QMainWindow(FBaseWindow):
    """
    QMainWindow is a class derived from QMainWindow to provide custom methods
    and properties for handling graphical user interface (GUI) related operations
    in the application.
    """

    def __init__(self, parent=None, *args, **kwargs):
        """
        Initializes the QMainWindow instance.

        :param parent: Parent QWidget. Defaults to None.
        """
        super(QMainWindow, self).__init__(parent, *args, **kwargs)
        QLabel.dispImage = dispImage
        self.styles = BaseStyle()
        self.tipWidget = MultiTipWidget(self, font_family="Microsoft YaHei", font_size=24)
        self.executor = ThreadPoolExecutor(max_workers=4)

    def clearUI(self):
        """
        Clears the UI and reloads settings from a YAML file.
        """
        pass

    def setConfig(self):
        """
        Method to set the configuration of the application. The actual implementation needs to be provided.
        """
        pass

    def loadStyleSheet(self, qssFilePath, base_path="./"):
        """
        Loads a QSS style sheet for the application from a given file path.

        :param qssFilePath: Path of the QSS file.
        :param base_path: Base path for the QSS file, defaults to the current directory.
        """
        loadQssStyles(window=self, qss_file=qssFilePath, base_path=base_path)

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Handles the close event of the main window.

        This method ensures proper cleanup of resources by:
        1. Shutting down the thread pool.
        2. Checking all attributes of the current instance (`self`) to identify those
           that inherit from `BaseDB` and calling their `close_db` method to close
           database connections if applicable.

        Args:
            event (QCloseEvent): The close event triggered when the window is being closed.

        Returns:
            None
        """
        # Shut down the thread pool
        self.executor.shutdown(wait=True)

        # Check and close any BaseDB instances
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, BaseDB):  # Check if the attribute is a BaseDB instance
                try:
                    attr.close()  # Call the close_db method
                except AttributeError:
                    print(f"Attribute {attr_name} does not have a close method.")

        # Automatically resolves to parent class's closeEvent
        super().closeEvent(event)

    def setNamedStyle(self, style_name='STYLE_TRANS'):
        """
        Apply a predefined style to the widget.

        Args:
            style_name (str): The name of the predefined style to apply. Available styles are:
                - 'STYLE_TRANS': Black transition style.
                - 'STYLE_LOGIN': White login style.
                - 'STYLE_NORM': Black normal style.
                - 'NORM_WHITE': White normal style.
                - 'NORM_GREEN': Green main style.
                - 'NormDark': Dark style.
                - 'MacOS': MacOS style.
                - 'Ubuntu': Ubuntu style.
                - 'ElegantDark': Elegant dark style.
                - 'Aqua': Aqua style.
                - 'NeonButtons': Neon buttons style.
                - 'NeonBlack': Neon black style.
                - 'BlueGlass': Blue glass style.
                - 'Dracula': Dracula (dark) style.
                - 'NightEyes': Night eyes style.
                - 'Parchment': Parchment style.
                - 'DarkVs15': Dark Visual Studio 2015 style.
                - 'DarkGreen': Dark green style.
                - 'DarkOrange': Dark orange style.
                - 'DarkPink': Dark pink style.
                - 'DarkPurple': Dark purple style.
                - 'DarkRed': Dark red style.
                - 'DarkYellow': Dark yellow style.
                - 'Skyrim': Skyrim style.
                - 'LightStyle': Light style.

        Raises:
            TypeError: If the style name is not a string.
            ValueError: If the style name is not found in predefined styles and is not a valid file path.
        """
        self.styles.set_named_style(self, style_name)

    def setStyleText(self, style_text):
        """
        Apply a given style text to a widget.

        Args:
            style_text: The style text to apply.
        """
        self.styles.set_style_text(self, style_text)

    def loadYamlSettings(self, yaml_file, base_path="./"):
        """
        Load settings for a QWidget from a YAML file and apply them to the specified window.

        Args:
            yaml_file (str): The file path of the YAML file containing the settings.
            base_path (str, optional): The base path used for resolving relative paths. Default is None.
        """
        loadYamlSettings(self, yaml_file, base_path)


class QLoginDialog(FLoginDialog):
    """
    A custom QDialog class representing a Login Dialog in a GUI application. This class inherits from QDialog.
    """

    def __init__(self, parent=None, *args, **kwargs):
        super(QLoginDialog, self).__init__(parent, *args, **kwargs)
        self.styles = BaseStyle()

    def loadStyleSheet(self, qssFilePath, base_path="./"):
        """
        Loads a QSS style sheet for the application from a given file path.

        :param qssFilePath: Path of the QSS file.
        :param base_path: Base path for the QSS file, defaults to the current directory.
        """
        loadQssStyles(window=self, qss_file=qssFilePath, base_path=base_path)

    def loadYamlSettings(self, yaml_file, base_path="./"):
        """
        Load settings for a QWidget from a YAML file and apply them to the specified window.

        Args:
            yaml_file (str): The file path of the YAML file containing the settings.
            base_path (str, optional): The base path used for resolving relative paths. Default is None.
        """
        loadYamlSettings(self, yaml_file, base_path)

    def setNamedStyle(self, style_name='STYLE_TRANS'):
        """
        Apply a predefined style to the widget.

        Args:
            style_name (str): The name of the predefined style to apply. Available styles are:
                - 'STYLE_TRANS': Black transition style.
                - 'STYLE_LOGIN': White login style.
                - 'STYLE_NORM': Black normal style.
                - 'NORM_WHITE': White normal style.
                - 'NORM_GREEN': Green main style.
                - 'NormDark': Dark style.
                - 'MacOS': MacOS style.
                - 'Ubuntu': Ubuntu style.
                - 'ElegantDark': Elegant dark style.
                - 'Aqua': Aqua style.
                - 'NeonButtons': Neon buttons style.
                - 'NeonBlack': Neon black style.
                - 'BlueGlass': Blue glass style.
                - 'Dracula': Dracula (dark) style.
                - 'NightEyes': Night eyes style.
                - 'Parchment': Parchment style.
                - 'DarkVs15': Dark Visual Studio 2015 style.
                - 'DarkGreen': Dark green style.
                - 'DarkOrange': Dark orange style.
                - 'DarkPink': Dark pink style.
                - 'DarkPurple': Dark purple style.
                - 'DarkRed': Dark red style.
                - 'DarkYellow': Dark yellow style.
                - 'Skyrim': Skyrim style.
                - 'LightStyle': Light style.

        Raises:
            TypeError: If the style name is not a string.
            ValueError: If the style name is not found in predefined styles and is not a valid file path.
        """
        self.styles.set_named_style(self, style_name)

    def setStyleText(self, style_text):
        """
        Apply a given style text to a widget.

        Args:
            style_text: The style text to apply.
        """
        self.styles.set_style_text(self, style_text)


class QImageLabel(FImageLabel):
    """
    A QLabel extension that provides additional functionality for displaying images.

    This class extends QLabel, providing the ability to display images and text. It allows for interactive
    manipulation of the image being displayed. This includes the ability to scale the image in and out using the mouse
    wheel (zooming), as well as panning the image by clicking and dragging with the mouse.

    The class also provides a set of buttons for image scaling: resetting to the original size, and increasing or
    decreasing the size by 10%.
    """

    def __init__(self, parent=None, *args, **kwargs):
        """
        Initializes the QImageLabel instance.

        :param parent: The parent widget to the label. Default is None.
        """
        super(QImageLabel, self).__init__(parent, *args, **kwargs)

    def loadStyleSheet(self, qssFilePath, base_path="./"):
        """
        Loads a QSS style sheet for the application from a given file path.

        :param qssFilePath: Path of the QSS file.
        :param base_path: Base path for the QSS file, defaults to the current directory.
        """
        loadQssStyles(window=self, qss_file=qssFilePath, base_path=base_path)


class QWindowCtrls(FWindowCtrls):
    """
    This class represents a main window with custom controls, including close, minimize, and hint buttons.
    Inherits from QMainWindow.
    """

    def __init__(self, main_window, exit_title, exit_message, icon=AVATAR,
                 button_sizes=(20, 20),
                 button_gaps=30, button_right_margin=80, hint_flag=False):
        """
        Initializes the FWindowCtrls instance.

        :param main_window: Reference to the main window.
        :param exit_title: The title for the exit message box.
        :param exit_message: The message for the exit message box.
        :param icon: The default icon for the window.
        :param button_sizes: Tuple representing the sizes of the buttons.
        :param button_gaps: The gaps between the buttons.
        :param button_right_margin: The right margin for the buttons.
        :param hint_flag: Flag to control hint visibility.
        """

        super(QWindowCtrls, self).__init__(main_window, exit_title, exit_message, icon=icon, button_sizes=button_sizes,
                                           button_gaps=button_gaps, button_right_margin=button_right_margin,
                                           hint_flag=hint_flag)

    def loadStyleSheet(self, qssFilePath, base_path="./"):
        """
        Loads a QSS style sheet for the application from a given file path.

        :param qssFilePath: Path of the QSS file.
        :param base_path: Base path for the QSS file, defaults to the current directory.
        """
        loadQssStyles(window=self, qss_file=qssFilePath, base_path=base_path)


class QMessageBox(FMessageBox):
    """
    This class represents a custom message box that inherits from QDialog.
    The message box includes a title, a message, and Yes/No buttons.
    """

    def __init__(self, title="Message Box", message="", yes_text="Yes", no_text="No", hint_flag=True, parent=None):
        """
        Initializes the QMessageBox instance.

        :param title: The title of the message box.
        :param message: The message to display.
        :param yes_text: The text for the Yes button.
        :param no_text: The text for the No button.
        :param hint_flag: Flag to control frame visibility.
        :param parent: The parent widget.
        """
        super(QMessageBox, self).__init__(title=title, message=message, yes_text=yes_text, no_text=no_text,
                                          hint_flag=hint_flag, parent=parent)
        self.styles = BaseStyle()

    def loadStyleSheet(self, qssFilePath, base_path="./"):
        """
        Loads a QSS style sheet for the application from a given file path.

        :param qssFilePath: Path of the QSS file.
        :param base_path: Base path for the QSS file, defaults to the current directory.
        """
        loadQssStyles(window=self, qss_file=qssFilePath, base_path=base_path)

    def setNamedStyle(self, style_name='STYLE_TRANS'):
        """
        Apply a predefined style to the widget.

        Args:
            style_name (str): The name of the predefined style to apply. Available styles are:
                - 'STYLE_TRANS': Black transition style.
                - 'STYLE_LOGIN': White login style.
                - 'STYLE_NORM': Black normal style.
                - 'NORM_WHITE': White normal style.
                - 'NORM_GREEN': Green main style.
                - 'NormDark': Dark style.
                - 'MacOS': MacOS style.
                - 'Ubuntu': Ubuntu style.
                - 'ElegantDark': Elegant dark style.
                - 'Aqua': Aqua style.
                - 'NeonButtons': Neon buttons style.
                - 'NeonBlack': Neon black style.
                - 'BlueGlass': Blue glass style.
                - 'Dracula': Dracula (dark) style.
                - 'NightEyes': Night eyes style.
                - 'Parchment': Parchment style.
                - 'DarkVs15': Dark Visual Studio 2015 style.
                - 'DarkGreen': Dark green style.
                - 'DarkOrange': Dark orange style.
                - 'DarkPink': Dark pink style.
                - 'DarkPurple': Dark purple style.
                - 'DarkRed': Dark red style.
                - 'DarkYellow': Dark yellow style.
                - 'Skyrim': Skyrim style.
                - 'LightStyle': Light style.

        Raises:
            TypeError: If the style name is not a string.
            ValueError: If the style name is not found in predefined styles and is not a valid file path.
        """
        self.styles.set_named_style(self, style_name)

    def setStyleText(self, style_text):
        """
        Apply a given style text to a widget.

        Args:
            style_text: The style text to apply.
        """
        self.styles.set_style_text(self, style_text)


def QSkinCtrls(
        parent: Optional[QWidget] = None, yaml_path: str = "", geometry: Optional[Tuple[int, int, int, int]] = None,
        text: str = "", icon_path: str = "", hidden: bool = False, style_qss: Optional[str] = None) -> QPushButton:
    """
    Create a modern "skin" button with a background image, transparent background,
    and dynamic border/padding effects on hover and click.
    When clicked, it will pop up SettingsDialog internally.

    Args:
        parent (QWidget): The parent widget to attach this button to. Defaults to None.
        yaml_path (str): A YAML file path, used in the default click handler.
        geometry (Tuple[int, int, int, int], optional): A tuple containing
            (pos_x, pos_y, width, height). If None, the button is placed
            at the top-right corner of the parent with a default size of (40, 40).
        text (str): The text displayed on the button. Defaults to "" (no text).
        icon_path (str): Path to the button's background image. Defaults to "" (no image).
        hidden (bool): Whether the button is initially hidden. Defaults to False.
        style_qss (str, optional): Custom QSS stylesheet string. If None, a default modern style is used.

    Returns:
        QPushButton: The created button with the specified properties.
    """

    # ======= Parameter Validation =======

    # Validate parent
    if parent is not None and not isinstance(parent, QWidget):
        raise TypeError("parent must be a QWidget (or None).")

    # Validate yaml_path
    if yaml_path:
        if not isinstance(yaml_path, str):
            raise TypeError("yaml_path must be a string.")
        if not os.path.isfile(yaml_path):
            raise FileNotFoundError(f"The specified yaml_path does not exist: {yaml_path}")

    # Validate geometry
    if geometry is not None:
        if not (isinstance(geometry, tuple) and len(geometry) == 4):
            raise TypeError("geometry must be a tuple of four integers: (pos_x, pos_y, width, height).")
        for idx, param in enumerate(geometry):
            if not isinstance(param, int):
                raise TypeError(f"geometry element {idx} must be an integer.")
            if param < 0:
                raise ValueError(f"geometry element {idx} must be a non-negative integer.")

    # Validate text
    if not isinstance(text, str):
        raise TypeError("text must be a string.")

    # Validate icon_path
    if icon_path:
        if not isinstance(icon_path, str):
            raise TypeError("icon_path must be a string.")
        if not os.path.isfile(icon_path):
            raise FileNotFoundError(f"The specified icon_path does not exist: {icon_path}")

    # Validate hidden
    if not isinstance(hidden, bool):
        raise TypeError("hidden must be a boolean.")

    # Validate style_qss
    if style_qss is not None and not isinstance(style_qss, str):
        raise TypeError("style_qss must be a string or None.")

    # ======= Create Button =======
    btn = QPushButton(text, parent)

    # Set background image using border-image if provided, else set default background
    if icon_path:
        if os.path.isfile(icon_path):
            background_image = icon_path.replace("\\", "/")  # Ensure correct path format
            background_image_url = f"url({background_image})"
        else:
            raise FileNotFoundError(f"Default background image not found at: {icon_path}")
    else:
        default_background_path = ":/default_icons/skins/skin_blue.png"
        background_image = default_background_path.replace("\\", "/")
        background_image_url = f"url({background_image})"

    # Determine button position and size
    if geometry is not None:
        pos_x, pos_y, width, height = geometry
    else:
        # Default size
        width, height = 30, 30
        if parent is not None:
            parent_width = parent.width()
            pos_x = parent_width - width - 160  # margin from the right
            pos_y = 15  # margin from the top
        else:
            # If no parent, default to (0,0)
            pos_x, pos_y = 0, 0

    # Set geometry
    btn.setGeometry(pos_x, pos_y, width, height)

    # Set visibility
    btn.setVisible(not hidden)

    # ======= Connect Click Event =======
    def on_skin_button_clicked():
        if not yaml_path:
            QMessageBox.warning(parent, "Warning", "No yaml_path provided. Cannot open SettingsDialog.")
            return
        dlg = SettingsDialog(yaml_path, parent)
        dlg.exec()
        loadYamlSettings(parent, yaml_file=yaml_path)

    btn.clicked.connect(on_skin_button_clicked)

    # ======= Set Stylesheet =======
    default_qss = f"""
    QPushButton {{
        border: none;
        border-image: {background_image_url} 0 0 0 0 stretch stretch;
        background-color: transparent;
        padding: 0px;
        border-radius: 8px;
        transition: border 0.3s, padding 0.3s, transform 0.2s;
    }}
    QPushButton:hover {{
        border: 2px solid #81A1C1;
        padding: 2px;
        transform: scale(1.05);
    }}
    QPushButton:pressed {{
        border: 2px solid #BF616A;
        padding: 2px;
        transform: scale(0.95);
    }}
    QPushButton:disabled {{
        border: none;
        background-color: transparent;
        opacity: 0.5;
    }}
    """

    if style_qss is None:
        btn.setStyleSheet(default_qss)
    else:
        btn.setStyleSheet(style_qss)

    # ======= Additional Enhancements =======
    # Set tooltip for better UX
    btn.setToolTip("Open Settings")

    # Enable mouse tracking for hover effects without clicking
    btn.setMouseTracking(True)

    return btn


def QConfigCtrls(
    parent: Optional[QWidget] = None,
    yaml_path: str = "",
    geometry: Optional[Tuple[int, int, int, int]] = None,
    text: str = "",
    icon_path: str = "",
    hidden: bool = False,
    style_qss: Optional[str] = None
) -> QPushButton:
    """
    Create a button that opens the ConfigDialog when clicked.

    Args:
        parent (Optional[QWidget]): The parent widget. Defaults to None.
        yaml_path (str): Path to the YAML configuration file.
        geometry (Optional[Tuple[int, int, int, int]]): The position and size (x, y, width, height).
            If None, default position and size are used.
        text (str): The text displayed on the button. Defaults to an empty string.
        icon_path (str): Path to the button's icon image. Defaults to an empty string.
        hidden (bool): Whether the button is initially hidden. Defaults to False.
        style_qss (Optional[str]): Custom QSS stylesheet string. If None, a default style is used.

    Returns:
        QPushButton: The created settings button.
    """
    # ======= Parameter Validation =======

    # Validate parent
    if parent is not None and not isinstance(parent, QWidget):
        raise TypeError("parent must be a QWidget or None.")

    # Validate yaml_path
    if yaml_path:
        if not isinstance(yaml_path, str):
            raise TypeError("yaml_path must be a string.")
        if not os.path.isfile(yaml_path):
            raise FileNotFoundError(f"The specified yaml_path does not exist: {yaml_path}")

    # Validate geometry
    if geometry is not None:
        if not (isinstance(geometry, tuple) and len(geometry) == 4):
            raise TypeError("geometry must be a tuple of four integers: (x, y, width, height).")
        for idx, param in enumerate(geometry):
            if not isinstance(param, int):
                raise TypeError(f"geometry element {idx} must be an integer.")
            if param < 0:
                raise ValueError(f"geometry element {idx} must be a non-negative integer.")

    # Validate text
    if not isinstance(text, str):
        raise TypeError("text must be a string.")

    # Validate icon_path
    if icon_path:
        if not isinstance(icon_path, str):
            raise TypeError("icon_path must be a string.")
        if not os.path.isfile(icon_path):
            raise FileNotFoundError(f"The specified icon_path does not exist: {icon_path}")

    # Validate hidden
    if not isinstance(hidden, bool):
        raise TypeError("hidden must be a boolean.")

    # Validate style_qss
    if style_qss is not None and not isinstance(style_qss, str):
        raise TypeError("style_qss must be a string or None.")

    # ======= Create Button =======
    btn = QPushButton(text, parent)

    # Set background image using border-image if provided, else set default background
    if icon_path:
        if os.path.isfile(icon_path):
            background_image = icon_path.replace("\\", "/")  # Ensure correct path format
            background_image_url = f"url({background_image})"
        else:
            raise FileNotFoundError(f"Default background image not found at: {icon_path}")
    else:
        default_background_path = ":/default_icons/skins/setting_std_blue.png"  # Replace with actual default icon path
        background_image = default_background_path.replace("\\", "/")
        background_image_url = f"url({background_image})"

    # Determine button position and size
    if geometry is not None:
        pos_x, pos_y, width, height = geometry
    else:
        # Default size
        width, height = 30, 30
        if parent is not None:
            parent_width = parent.width()
            pos_x = parent_width - width - 200  # Margin from the right
            pos_y = 15  # Margin from the top
        else:
            # If no parent, default to (0,0)
            pos_x, pos_y = 0, 0

    # Set geometry
    btn.setGeometry(pos_x, pos_y, width, height)

    # Set visibility
    btn.setVisible(not hidden)

    # ======= Connect Click Event =======
    def on_settings_button_clicked() -> None:
        """
        Slot function to handle settings button click.
        Opens the ConfigDialog.
        """
        if not yaml_path:
            QMessageBox.warning(parent, "Warning", "No yaml_path provided. Cannot open configuration window.")
            return
        try:
            dlg = ConfigDialog(yaml_path, parent)
            if dlg.exec() == QDialog.Accepted:
                # Optionally, perform actions after successful configuration
                pass
                # QMessageBox.information(parent, "Information", "Configuration has been updated.")
        except Exception as e:
            QMessageBox.critical(parent, "Error", f"Failed to open configuration window: {e}")

    btn.clicked.connect(on_settings_button_clicked)

    # ======= Set Stylesheet =======
    default_qss = f"""
    QPushButton {{
        border: none;
        border-image: {background_image_url} 0 0 0 0 stretch stretch;
        background-color: transparent;
        padding: 0px;
        border-radius: 8px;
        transition: border 0.3s, padding 0.3s, transform 0.2s;
    }}
    QPushButton:hover {{
        border: 2px solid #81A1C1;
        padding: 2px;
        transform: scale(1.05);
    }}
    QPushButton:pressed {{
        border: 2px solid #BF616A;
        padding: 2px;
        transform: scale(0.95);
    }}
    QPushButton:disabled {{
        border: none;
        background-color: transparent;
        opacity: 0.5;
    }}
    """

    if style_qss is None:
        btn.setStyleSheet(default_qss)
    else:
        btn.setStyleSheet(style_qss)

    # ======= Additional Enhancements =======
    # Set tooltip for better UX
    btn.setToolTip("Open Configuration Settings")

    # Enable mouse tracking for hover effects without clicking
    btn.setMouseTracking(True)

    return btn
