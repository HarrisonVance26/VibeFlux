# VibeFlux, AGPL-3.0 license
import os

import cv2
from ..base.Extension import IMageLabel, IMessageBox, IMExtWindow
from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QToolButton, QMessageBox, QApplication, QPushButton, QDialog

from .. import __package_name__
from ..config.QfConfig import QF_Config

AVATAR = ":/default_icons/default_avatar.png"
HOME = ":/default_icons/home.png"
BIG_SIZE = ":/default_icons/bigsize.png"
SMALL_SIZE = ":/default_icons/smallsize.png"

WINDOW_CONTROL_ICONS = {
    "windows": {
        "close": {
            "normal": ":/default_icons/window_controls/windows_close.svg",
            "hover": ":/default_icons/window_controls/windows_close_hover.svg",
            "pressed": ":/default_icons/window_controls/windows_close_pressed.svg",
        },
        "maximize": {
            "normal": ":/default_icons/window_controls/windows_maximize.svg",
            "hover": ":/default_icons/window_controls/windows_maximize_hover.svg",
            "pressed": ":/default_icons/window_controls/windows_maximize_pressed.svg",
        },
        "minimize": {
            "normal": ":/default_icons/window_controls/windows_minimize.svg",
            "hover": ":/default_icons/window_controls/windows_minimize_hover.svg",
            "pressed": ":/default_icons/window_controls/windows_minimize_pressed.svg",
        },
        "restore": {
            "normal": ":/default_icons/window_controls/windows_restore.svg",
            "hover": ":/default_icons/window_controls/windows_restore_hover.svg",
            "pressed": ":/default_icons/window_controls/windows_restore_pressed.svg",
        },
    },
}


class FImageLabel(IMageLabel):
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
        Initializes the FImageLabel instance.

        :param parent: The parent widget to the label. Default is None.
        """
        super(FImageLabel, self).__init__(parent, *args, **kwargs)
        self.init_ui()  # Initialize UI

    def setAspectMode(self, keepAspect: bool):
        """
        Sets the aspect ratio mode for the label.

        :param keepAspect: If True, the aspect ratio is maintained.
        """
        super().setAspectMode(keepAspect)

    def init_ui(self):
        """
        Initializes the user interface (UI) of the label.
        """

        self.setWindowTitle("ImageBox")
        self.setStyleSheet("QFrame{border:1px solid #44cef6;\n"
                           "background-color: transparent;}")
        self.boxToolButton()  # Initialize the toolbar buttons

    def dispImage(self, image, keepAspect=True):
        """
        Displays an image read by OpenCV in the label.

        :param image: The image to display.
        :param keepAspect: If True, the aspect ratio of the image is maintained.
        """
        show = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert the image to RGB
        super().dispImage(show, keepAspect)

    def dispText(self, text):
        """
        Displays text in the label.

        :param text: The text to display.
        """
        super().dispText(text)

    def paintEvent(self, e):
        """
        Handles paint events.

        :param e: The paint event.
        """
        super().paintEvent(e)

    def wheelEvent(self, event):
        """
        Handles mouse wheel events. This will allow to zoom the image in or out.

        :param event: The wheel event.
        """
        super().wheelEvent(event)

    def mouseMoveEvent(self, e):
        """
        Handles mouse move events. This will allow to pan the image when the mouse is moved.

        :param e: The mouse event.
        """
        super().mouseMoveEvent(e)

    def mousePressEvent(self, e):
        """
        Handles mouse press events. This will start the panning operation.

        :param e: The mouse event.
        """
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        """
        Handles mouse release events. This will end the panning operation.

        :param e: The mouse event.
        """
        super().mouseReleaseEvent(e)

    def boxToolButton(self, button_size=25):
        """
        Sets up the buttons for the tool bar.

        :param button_size: The size of the buttons.
        """

        button_normal = QToolButton(self)
        button_normal.move(self.geometry().x(), self.geometry().y())
        button_normal.setFixedSize(button_size, button_size)
        button_normal.setStyleSheet("""QToolButton{background-color: transparent;border-image: none;}
                                    QToolButton::hover{border: 0px;} """)
        icon = QtGui.QIcon()
        icon.addPixmap(QPixmap(HOME), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button_normal.setIcon(icon)
        button_normal.setIconSize(QtCore.QSize(button_size, button_size))
        button_normal.clicked.connect(self.normButton)

        button_bigger = QToolButton(self)
        pos = self.geometry().x() + button_size + 10, self.geometry().y()
        button_bigger.move(pos[0], pos[1])
        button_bigger.setFixedSize(button_size, button_size)
        button_bigger.setStyleSheet("""QToolButton{background-color: transparent;border-image: none;}
                                        QToolButton::hover{border: 0px;} """)
        icon = QtGui.QIcon()
        icon.addPixmap(QPixmap(BIG_SIZE), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button_bigger.setIcon(icon)
        button_bigger.setIconSize(QtCore.QSize(button_size, button_size))
        button_bigger.clicked.connect(self.bigButton)

        button_smaller = QToolButton(self)
        button_smaller.move(pos[0] + button_size + 10, pos[1])
        button_smaller.setFixedSize(button_size, button_size)
        button_smaller.setStyleSheet("""QToolButton{background-color: transparent;border-image: none;}
                                       QToolButton::hover{border: 0px;} """)
        icon = QtGui.QIcon()
        icon.addPixmap(QPixmap(SMALL_SIZE), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        button_smaller.setIcon(icon)
        button_smaller.setIconSize(QtCore.QSize(button_size, button_size))
        button_smaller.clicked.connect(self.smallButton)

    def normButton(self):
        """
        Resets the image size to the original size.
        """
        super().normButton()

    def bigButton(self):
        """
        Increases the size of the image by 10%.
        """
        super().bigButton()

    def smallButton(self):
        """
        Decreases the size of the image by 10%.
        """
        super().smallButton()


class FWindowCtrls(IMExtWindow):
    """
    This class represents a main window with custom controls, including close, minimize, and hint buttons.
    Inherits from QMainWindow.
    """

    def __init__(self, main_window, exit_title, exit_message, icon=AVATAR,
                 button_sizes=(20, 20),
                 button_gaps=30, button_right_margin=80, hint_flag=False,
                 button_style="macos", max_button_mode="maximize",
                 button_icons=None, button_icon_size=None, button_top_margin=20):
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
        :param button_style: Window button style. Available values are 'macos' and 'windows'.
        :param max_button_mode: Max button behavior. Available values are 'maximize' and 'fullscreen'.
        :param button_icons: Optional icon mapping for themed window buttons.
        :param button_icon_size: Optional icon size for icon-based button styles.
        :param button_top_margin: The top margin for the buttons.
        """

        super().__init__(main_window)
        self.verbose = QF_Config.VERBOSE
        self.msg_box = None  # Message box instance
        self.main_window = main_window  # Reference to the main window
        self.hint_flag = hint_flag  # Flag to control hint visibility
        self.exit_title = exit_title  # Exit message box title
        self.exit_message = exit_message  # Exit message box message
        self.icon = icon  # Default icon for the window
        self.button_right_margin = button_right_margin  # Right margin for the buttons
        self.button_gaps = button_gaps  # Gaps between buttons
        self.button_sizes = button_sizes  # Sizes of buttons
        self.button_style = button_style  # Style name for the window control buttons
        self.max_button_mode = max_button_mode  # Maximize or fullscreen behavior
        self.button_icons = button_icons or {}  # Optional icon overrides for title bar buttons
        self.button_icon_size = button_icon_size  # Icon size for button styles that use icons
        self.button_top_margin = button_top_margin  # Top margin for title bar buttons
        self._normal_geometry = None  # Normal geometry before maximizing
        self._normal_maximum_size = None  # Normal maximum size before maximizing
        self.button_close = None  # Close button instance
        self.button_max = None  # Maximize or fullscreen button instance
        self.button_min = None  # Minimize button instance
        self._button_icon_paths = {}  # Button to icon-state mapping
        self._window_control_icons = {}  # Normalized icon resources for the selected style
        self._prepare_button_style()  # Normalize style-related settings
        self.setupWindowControls()  # Initialize window controls
        self.main_window.installEventFilter(self)  # Keep title bar controls aligned after resizing

    def closeQButton(self):
        """
        Method to create a QMessageBox on closing the application.
        """
        reply = QMessageBox.question(self.main_window, self.exit_title, self.exit_message,
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event = QApplication.instance()
            event.quit()  # Quit the application
            if self.verbose:
                print(f"{__package_name__} Closed...")
            else:
                print("Closed...")
        else:
            return

    def setMessageBox(self, title="Message Box", message="Are you sure you want to quit?", yes_text="Yes", no_text="No",
                      hint_flag=False, icon=HOME):
        """
        Method to set a custom message box.

        :param title: The title of the message box.
        :param message: The message in the message box.
        :param yes_text: The text for the Yes button.
        :param no_text: The text for the No button.
        :param hint_flag: Flag for hint visibility.
        :param icon: Icon for the message box.
        """
        self.msg_box = FMessageBox(title=title, message=message, yes_text=yes_text, no_text=no_text,
                                   hint_flag=hint_flag)
        self.msg_box.set_icon(icon)  # Set the icon for the message box

    def closeButton(self):
        """
        Method to handle the close button event.
        """
        if self.msg_box is None:
            self.msg_box = FMessageBox(title=self.exit_title, message=self.exit_message, hint_flag=self.hint_flag)
            self.msg_box.set_icon(self.icon)

        # Ensure that the size of the message box is set
        self.msg_box.adjustSize()

        # Get the geometry of the main window and the message box
        mw_frame = self.main_window.frameGeometry()
        msg_box_frame = self.msg_box.frameGeometry()

        # Calculate and set the position of the message box
        center_point = mw_frame.center() - QPoint(msg_box_frame.width() / 2, msg_box_frame.height() / 2)
        self.msg_box.move(center_point)

        reply = self.msg_box.result()
        if reply == QDialog.Accepted:
            event = QApplication.instance()
            event.quit()  # Quit the application
            if self.verbose:
                print(f"{__package_name__} Closed...")
            else:
                print("Closed...")
        else:
            return

    def minButton(self):
        """
        Method to minimize the main window.
        """
        self.main_window.showMinimized()

    def maxButton(self):
        """
        Method to maximize, fullscreen, or restore the main window.
        """
        if self.main_window.isMaximized() or self.main_window.isFullScreen():
            if self._normal_maximum_size is not None:
                self.main_window.setMaximumSize(self._normal_maximum_size)
            self.main_window.showNormal()
            if self._normal_geometry is not None:
                self.main_window.setGeometry(self._normal_geometry)
            self._set_max_button_text(maximized=False)
            return

        self._normal_geometry = self.main_window.geometry()
        self._normal_maximum_size = self.main_window.maximumSize()
        self.main_window.setMaximumSize(16777215, 16777215)
        if str(self.max_button_mode).lower() == "fullscreen":
            self.main_window.showFullScreen()
        else:
            self.main_window.showMaximized()
        self._set_max_button_text(maximized=True)

    def hintButton(self):
        """
        Method to handle the hint button event.

        This method is kept for backward compatibility. It now delegates to maxButton.
        """
        self.maxButton()

    def _prepare_button_style(self):
        """
        Normalizes button style settings before creating the controls.
        """
        style_name = str(self.button_style).strip().lower()
        if style_name in ("win", "windows"):
            self.button_style = "windows"
            if self.button_sizes == (20, 20):
                self.button_sizes = (52, 34)
            if self.button_gaps == 30:
                self.button_gaps = self.button_sizes[0]
            if self.button_icon_size is None:
                self.button_icon_size = (17, 17)
        else:
            self.button_style = "macos"
        self._window_control_icons = self._prepare_window_control_icons()

    def _prepare_window_control_icons(self):
        """
        Returns icon resources for the current button style.
        """
        defaults = WINDOW_CONTROL_ICONS.get(self.button_style, {})
        icons = {
            role: dict(states)
            for role, states in defaults.items()
        }
        for role, states in self.button_icons.items():
            if isinstance(states, str):
                icons[role] = {"normal": states}
            elif isinstance(states, dict):
                role_icons = icons.setdefault(role, {})
                role_icons.update(states)
        return icons

    def _resource_to_file_path(self, resource_path):
        """
        Converts a VibeFlux qrc resource path to a packaged file path.
        """
        if not isinstance(resource_path, str) or not resource_path.startswith(":/"):
            return resource_path
        package_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        relative_path = resource_path[2:].replace("/", os.sep)
        return os.path.join(package_dir, relative_path)

    def _make_icon(self, resource_path):
        """
        Creates an icon from qrc first, then falls back to the packaged file path.
        """
        icon = QtGui.QIcon(resource_path)
        if icon.isNull():
            fallback_path = self._resource_to_file_path(resource_path)
            if fallback_path and os.path.exists(fallback_path):
                icon = QtGui.QIcon(fallback_path)
        return icon

    def _register_control_icon(self, button, role):
        """
        Registers state-aware icons for a title bar button.
        """
        states = self._window_control_icons.get(role, {})
        if not states:
            return
        install_filter = button not in self._button_icon_paths
        self._button_icon_paths[button] = states
        button.setText("")
        if self.button_icon_size:
            if isinstance(self.button_icon_size, QtCore.QSize):
                icon_size = self.button_icon_size
            elif isinstance(self.button_icon_size, int):
                icon_size = QtCore.QSize(self.button_icon_size, self.button_icon_size)
            else:
                icon_size = QtCore.QSize(self.button_icon_size[0], self.button_icon_size[1])
            button.setIconSize(icon_size)
        self._apply_control_icon(button, "normal")
        if install_filter:
            button.installEventFilter(self)

    def _apply_control_icon(self, button, state):
        """
        Applies the icon for a state such as normal, hover, or pressed.
        """
        states = self._button_icon_paths.get(button, {})
        icon_path = states.get(state) or states.get("normal")
        if icon_path:
            button.setIcon(self._make_icon(icon_path))

    def eventFilter(self, watched, event):
        """
        Keeps icon colors in sync with title bar button hover and press states.
        """
        if watched is self.main_window and event.type() == QtCore.QEvent.Resize:
            self._update_window_control_positions()
        elif watched in self._button_icon_paths:
            event_type = event.type()
            if event_type == QtCore.QEvent.Enter:
                self._apply_control_icon(watched, "hover")
            elif event_type == QtCore.QEvent.Leave:
                self._apply_control_icon(watched, "normal")
            elif event_type == QtCore.QEvent.MouseButtonPress:
                self._apply_control_icon(watched, "pressed")
            elif event_type == QtCore.QEvent.MouseButtonRelease:
                self._apply_control_icon(watched, "hover" if watched.underMouse() else "normal")
        return super().eventFilter(watched, event)

    def _update_window_control_positions(self):
        """
        Reposition title bar buttons after the main window size changes.
        """
        if not all((self.button_close, self.button_max, self.button_min)):
            return
        pos_x = self.main_window.size().width()
        self.button_close.move(pos_x - self.button_right_margin, self.button_top_margin)
        self.button_max.move(pos_x - self.button_right_margin - self.button_gaps, self.button_top_margin)
        self.button_min.move(pos_x - self.button_right_margin - 2 * self.button_gaps, self.button_top_margin)

    def _macos_button_qss(self, color, hover_color):
        """
        Returns a macOS-like round button stylesheet.

        :param color: Normal background color.
        :param hover_color: Hover background color.
        :return: QSS stylesheet string.
        """
        radius = int(min(self.button_sizes) / 2)
        return ("QPushButton{\n"
                f"    background:{color};\n"
                "    color:white;\n"
                f"    box-shadow: 1px 1px 3px;border-radius: {radius}px;\n"
                "}\n"
                "QPushButton:hover{                    \n"
                f"    background:{hover_color};\n"
                "}\n"
                "QPushButton:pressed{\n"
                "    border: 1px solid #3C3C3C!important;\n"
                "    background:black;\n"
                "}")

    def _windows_button_qss(self, role="normal"):
        """
        Returns a Windows-like title bar button stylesheet.

        :param role: Button role, such as 'normal' or 'close'.
        :return: QSS stylesheet string.
        """
        if role == "close":
            hover_background = "#E81123"
            pressed_background = "#B0001B"
        else:
            hover_background = "rgba(0, 120, 215, 70)"
            pressed_background = "rgba(0, 120, 215, 120)"
        return ("QPushButton{\n"
                "    background:transparent;\n"
                "    border:none;\n"
                "    border-radius:0px;\n"
                "    padding:0px;\n"
                "}\n"
                "QPushButton:hover{\n"
                f"    background:{hover_background};\n"
                "}\n"
                "QPushButton:pressed{\n"
                f"    background:{pressed_background};\n"
                "}")

    def _set_max_button_text(self, maximized=False):
        """
        Updates the max button icon for styles that display icon resources.

        :param maximized: Whether the window is currently maximized or fullscreen.
        """
        if self.button_max is None or self.button_style != "windows":
            return
        self._register_control_icon(self.button_max, "restore" if maximized else "maximize")

    def setupWindowControls(self):
        """
        Method to set up window controls like buttons.
        """
        # Code for setting up and displaying the close button
        pos_x = self.main_window.size().width()
        button_red = QPushButton(self.main_window)
        button_red.move(pos_x - self.button_right_margin, self.button_top_margin)
        button_red.setFixedSize(self.button_sizes[0], self.button_sizes[1])
        if self.button_style == "windows":
            button_red.setStyleSheet(self._windows_button_qss(role="close"))
            self._register_control_icon(button_red, "close")
        else:
            button_red.setStyleSheet(self._macos_button_qss("#CE0000", "red"))
        button_red.setToolTip("Close")
        button_red.clicked.connect(self.closeButton)  # Connect the close button event
        self.button_close = button_red

        button_orange = QPushButton(self.main_window)
        button_orange.move(pos_x - self.button_right_margin - self.button_gaps, self.button_top_margin)
        button_orange.setFixedSize(self.button_sizes[0], self.button_sizes[1])
        if self.button_style == "windows":
            button_orange.setStyleSheet(self._windows_button_qss())
            self._register_control_icon(button_orange, "maximize")
        else:
            button_orange.setStyleSheet(self._macos_button_qss("orange", "yellow"))
        button_orange.setToolTip("Maximize/Restore")
        button_orange.clicked.connect(self.maxButton)
        self.button_max = button_orange

        button_green = QPushButton(self.main_window)
        button_green.move(pos_x - self.button_right_margin - 2 * self.button_gaps, self.button_top_margin)
        button_green.setFixedSize(self.button_sizes[0], self.button_sizes[1])
        if self.button_style == "windows":
            button_green.setStyleSheet(self._windows_button_qss())
            self._register_control_icon(button_green, "minimize")
        else:
            button_green.setStyleSheet(self._macos_button_qss("green", "#08BF14"))
        button_green.setToolTip("Minimize")
        button_green.clicked.connect(self.minButton)
        self.button_min = button_green


class FMessageBox(IMessageBox):
    """
    This class represents a custom message box that inherits from QDialog.
    The message box includes a title, a message, and Yes/No buttons.
    """

    def __init__(self, title="Message Box", message="", yes_text="Yes", no_text="No", hint_flag=True, parent=None):
        """
        Initializes the FMessageBox instance.

        :param title: The title of the message box.
        :param message: The message to display.
        :param yes_text: The text for the Yes button.
        :param no_text: The text for the No button.
        :param hint_flag: Flag to control frame visibility.
        :param parent: The parent widget.
        """
        super(FMessageBox, self).__init__(parent)

        self.setWindowTitle(title)  # Set the title of the message box

        if hint_flag:
            self.setWindowFlags(Qt.FramelessWindowHint)  # Removes the window frame if hint_flag is True

        self.layoutMessage(message, yes_text, no_text)

        # Apply the default QSS stylesheet
        self.set_stylesheet()

        # Connect the button clicked signals to the appropriate slots
        self.yes_button.clicked.connect(self.accept)
        self.no_button.clicked.connect(self.reject)

    def set_message(self, message):
        """
        Sets the message in the message box.

        :param message: The message to set.
        """
        self.message.setText(message)

    def set_icon(self, icon_path):
        """
        Sets the window icon.

        :param icon_path: The path to the icon file.
        """
        super().set_icon(icon_path)

    def result(self):
        """
        Executes the QDialog and returns the result.
        """
        return self.exec_()

    def set_stylesheet(self, stylesheet=None):
        """
        Sets the QSS stylesheet.

        :param stylesheet: The QSS stylesheet to apply. If None, the default stylesheet is used.
        """
        if stylesheet is None:
            stylesheet = """
                MessageBox {
                    background-color: rgba(255, 255, 255, 0.4);
                    border-radius: 10px;
                }
                QLabel {
                    color: black;
                    font-size: 20px;
                    text-align: center;
                }
                QPushButton {
                    color: #F0F0F0;
                    font-size: 20px;
                    background-color: #1E90FF;
                    border: none;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #3BB9FF;
                }
                QPushButton:pressed {
                    background-color: #1569C7;
                }
            """
        self.setStyleSheet(stylesheet)  # Apply the stylesheet
