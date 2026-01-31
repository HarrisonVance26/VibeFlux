import os
from typing import Optional, Tuple

from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication, QCursor
from PySide6.QtWidgets import QMainWindow, QDialog, QWidget, QPushButton, QMessageBox, QSpinBox, QDoubleSpinBox

import os
from typing import Dict, Any, Optional, Tuple

from PySide6.QtCore import QSize
from PySide6.QtWidgets import (QLabel, QFileDialog, QLineEdit, QGridLayout, QHBoxLayout, QVBoxLayout, QCheckBox,
                               QScrollArea, QGroupBox)
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq


class IMainWindow(QMainWindow):
    """
    FBaseWindow is a class derived from QMainWindow to provide custom methods
    and properties for handling graphical user interface (GUI) related operations
    in the application.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the FBaseWindow instance.

        :param parent: Parent QWidget. Defaults to None.
        """
        super(IMainWindow, self).__init__(*args, **kwargs)

    def setUiStyle(self, windowFlag=False, transBackFlag=False):
        """
        Sets UI styles and widget states based on the provided flags.

        :param windowFlag: If True, removes window border.
        :param transBackFlag: If True, sets window background to transparent.
        """
        if windowFlag:
            self.setWindowFlags(Qt.FramelessWindowHint)
        if transBackFlag:
            self.setAttribute(Qt.WA_TranslucentBackground)
        self.moveToCenter()  # move window to the center

    def styleSheet(self, user=None):
        if user == "Seasal":
            return super().styleSheet()
        else:
            return ""

    def moveToCenter(self):
        """
        Moves the current window to the center of the screen.
        """
        screen = QGuiApplication.primaryScreen().geometry()  # Get screen size
        size = self.geometry()  # Get current window size
        # Move window to center of screen
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def mousePressEvent(self, event):
        """
        Event handler for mouse press event.

        :param event: The mouse event.
        """
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        """
        Event handler for mouse move event.

        :param QMouseEvent: The mouse event.
        """
        try:
            if Qt.LeftButton and self.m_flag:
                self.move(QMouseEvent.globalPos() - self.m_Position)
                QMouseEvent.accept()
        except:
            pass

    def mouseReleaseEvent(self, QMouseEvent):
        """
        Event handler for mouse release event.

        :param QMouseEvent: The mouse event.
        """
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))


class IMDialog(QDialog):
    """
    A custom QDialog class representing a Login Dialog in a GUI application. This class inherits from QDialog.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the FLoginDialog instance.

        :param parent: The parent widget to the dialog. Default is None.
        """
        super(IMDialog, self).__init__(*args, **kwargs)

    def setSlots(self):
        """
        Method to define slots for the Login dialog.
        The actual implementation needs to be provided.
        """
        pass

    def set_tab_order(self, *widgets):
        """
        Sets the tab order for the given widgets.

        :param widgets: The widgets to set the tab order for.
        """
        for i in range(len(widgets) - 1):
            self.setTabOrder(widgets[i], widgets[i + 1])  # Set the tab order for the pair of widgets

    def setUiStyle(self, windowFlag=False, transBackFlag=False):
        """
        Sets the user interface style and widget states of the dialog.

        :param windowFlag: If True, removes the border of the dialog.
        :param transBackFlag: If True, makes the dialog's background transparent.
        """
        if windowFlag:
            self.setWindowFlags(Qt.FramelessWindowHint)  # Removes the border of the dialog
        if transBackFlag:
            self.setAttribute(Qt.WA_TranslucentBackground)  # Makes the dialog's background transparent

    def mousePressEvent(self, event):
        """
        Overriding the mousePressEvent for custom behavior.

        :param event: The mouse press event.
        """
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # Get the position of the mouse relative to the window
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # Change mouse icon to OpenHandCursor

    def mouseMoveEvent(self, QMouseEvent):
        """
        Overriding the mouseMoveEvent for custom behavior.

        :param QMouseEvent: The mouse move event.
        """
        try:
            if Qt.LeftButton and self.m_flag:
                self.move(QMouseEvent.globalPos() - self.m_Position)  # Change the window position
                QMouseEvent.accept()
        except:
            pass

    def mouseReleaseEvent(self, QMouseEvent):
        """
        Overriding the mouseReleaseEvent for custom behavior.

        :param QMouseEvent: The mouse release event.
        """
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))  # Change mouse icon to ArrowCursor

    def styleSheet(self, user=None):
        if user == "Seasal":
            return super().styleSheet()
        else:
            return ""


class IMSettingsDialog(QDialog):
    def __init__(self, yaml_path: str, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the SettingsDialog.

        Args:
            yaml_path (str): Path to the YAML configuration file.
            parent (Optional[QWidget], optional): Parent widget. Defaults to None.
        """
        super().__init__(parent)

        self.setWindowTitle("Interface Settings")
        self.yaml_path = yaml_path
        self.setMinimumSize(640, 480)

        # ===================== Style Enhancements =====================
        # Use QSS to beautify the dialog
        # self.styles = BaseStyle()
        # self.styles.set_named_style(self, style_name='LightStyle')
        # self.setStyleSheet("""""")

        self.yaml_parser = YAML()
        # Preserve original quotes
        self.yaml_parser.preserve_quotes = True
        # Use uppercase True/False when writing back boolean values
        self.yaml_parser.boolean_representation = {True: 'True', False: 'False'}

        # ===================== Load YAML Configuration =====================
        self.config_data = self.load_yaml(self.yaml_path)

        # edit_controls stores references to edit widgets for writing back on "Confirm"
        self.edit_controls: Dict[str, Dict[str, Optional[QWidget]]] = {}
        # browse_buttons manages "Browse" buttons uniformly -> (control_name, line_edit_key)
        self.browse_buttons: Dict[QPushButton, Tuple[str, str]] = {}

        # Main layout with scroll area
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)  # Reduced margins
        main_layout.setSpacing(8)  # Reduced spacing

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(8)  # Reduced spacing

        # Iterate over YAML and generate settings items
        for control_name, control_info in self.config_data.items():
            group_box = self.create_control_group(control_name, control_info)
            self.scroll_layout.addWidget(group_box)

        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

        # Bottom buttons (Confirm / Cancel)
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(16)  # Adjusted spacing between buttons

        btn_confirm = QPushButton("Confirm")
        btn_cancel = QPushButton("Cancel")
        btn_confirm.setMinimumWidth(80)
        btn_cancel.setMinimumWidth(80)
        btn_confirm.setMinimumHeight(25)  # Increased height
        btn_cancel.setMinimumHeight(25)  # Increased height
        btn_confirm.clicked.connect(self.save_and_close)
        btn_cancel.clicked.connect(self.close)

        btn_layout.addStretch()
        btn_layout.addWidget(btn_confirm)
        btn_layout.addWidget(btn_cancel)

        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def load_yaml(self, yaml_path: str) -> Dict[str, Any]:
        """
        Load YAML file using ruamel.yaml while preserving comments, order, and case.

        Args:
            yaml_path (str): Path to the YAML configuration file.

        Returns:
            Dict[str, Any]: Parsed YAML data.
        """
        if not os.path.exists(yaml_path):
            QMessageBox.warning(self, "Warning", f"Configuration file not found: {yaml_path}")
            return {}
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = self.yaml_parser.load(f)
            return data if data else {}

    def create_control_group(self, control_name: str, control_info: Dict[str, Any]) -> QGroupBox:
        """
        Create a QGroupBox for each control based on YAML configuration,
        dynamically generating "info" display (read-only), "enabled" checkbox,
        "type"/"text"/"icon"/"background"/"windowIcon", etc.

        Args:
            control_name (str): Name of the control.
            control_info (Dict[str, Any]): Configuration information for the control.

        Returns:
            QGroupBox: The created group box containing the control settings.
        """
        group_box = QGroupBox(control_name, self)
        # Apply stylesheet to the QGroupBox title
        group_box.setStyleSheet("""
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
                color: #00509E;                  /* Darker blue title text */
                font-size: 16px;                 /* Larger font size */
                font-weight: bold;               /* Bold text */
            }
        """)
        layout = QGridLayout(group_box)
        layout.setContentsMargins(8, 16, 8, 8)  # Reduced margins
        layout.setSpacing(8)  # Reduced spacing

        row = 0

        # 0) Info (if available, display text only, read-only)
        if "info" in control_info:
            lbl_info_label = QLabel("Info:", group_box)
            lbl_info_text = QLabel(str(control_info["info"]), group_box)
            lbl_info_text.setWordWrap(True)

            layout.addWidget(lbl_info_label, row, 0)
            layout.addWidget(lbl_info_text, row, 1, 1, 2)
            row += 1

        # 1) Enabled
        enabled_checkbox = QCheckBox("Enabled", group_box)
        enabled_state = control_info.get("enabled", True)
        enabled_checkbox.setChecked(enabled_state)

        # Set the QCheckBox's fixed size
        enabled_checkbox.setFixedSize(QSize(120, 30))  # Adjust width (120) and height (30) as needed

        # Set the QCheckBox's display text font size
        font = enabled_checkbox.font()
        font.setPointSize(12)  # Set the desired font size
        font.setBold(True)  # Make the text bold
        enabled_checkbox.setFont(font)

        # Add the QCheckBox to the layout
        layout.addWidget(enabled_checkbox, row, 0, 1, 3)
        row += 1

        # 2) Type
        type_lineedit: Optional[QLineEdit] = None
        if "type" in control_info:
            lbl_type = QLabel("Type:", group_box)
            type_lineedit = QLineEdit(str(control_info.get("type", "")), group_box)
            type_lineedit.setReadOnly(True)
            type_lineedit.setToolTip("Do not modify easily! If changes are needed, please edit manually.")
            layout.addWidget(lbl_type, row, 0)
            layout.addWidget(type_lineedit, row, 1, 1, 2)
            row += 1

        # 3) Text
        text_lineedit: Optional[QLineEdit] = None
        if "text" in control_info:
            lbl_text = QLabel("Text:", group_box)
            text_lineedit = QLineEdit(str(control_info.get("text", "")), group_box)
            layout.addWidget(lbl_text, row, 0)
            layout.addWidget(text_lineedit, row, 1, 1, 2)
            row += 1

        # 4) Icon
        icon_lineedit: Optional[QLineEdit] = None
        if "icon" in control_info:
            lbl_icon = QLabel("Icon:", group_box)
            icon_lineedit = QLineEdit(str(control_info.get("icon", "")), group_box)

            btn_browse_icon = QPushButton("Browse", group_box)
            btn_browse_icon.setMinimumWidth(70)
            btn_browse_icon.setMinimumHeight(20)  # Optional: Increase Browse button height
            layout.addWidget(lbl_icon, row, 0)
            layout.addWidget(icon_lineedit, row, 1)
            layout.addWidget(btn_browse_icon, row, 2)
            row += 1

            # Map the button to its corresponding line edit
            self.browse_buttons[btn_browse_icon] = (control_name, "icon_lineedit")
            btn_browse_icon.clicked.connect(self.on_browse_file)

        # 5) Background
        background_lineedit: Optional[QLineEdit] = None
        if "background" in control_info:
            lbl_bg = QLabel("Background:", group_box)
            background_lineedit = QLineEdit(str(control_info.get("background", "")), group_box)

            btn_browse_bg = QPushButton("Browse", group_box)
            btn_browse_bg.setMinimumWidth(70)
            btn_browse_bg.setMinimumHeight(20)  # Optional: Increase Browse button height
            layout.addWidget(lbl_bg, row, 0)
            layout.addWidget(background_lineedit, row, 1)
            layout.addWidget(btn_browse_bg, row, 2)
            row += 1

            self.browse_buttons[btn_browse_bg] = (control_name, "background_lineedit")
            btn_browse_bg.clicked.connect(self.on_browse_file)

        # 6) Window Icon
        windowicon_lineedit: Optional[QLineEdit] = None
        if "windowIcon" in control_info:
            lbl_wicon = QLabel("Window Icon:", group_box)
            windowicon_lineedit = QLineEdit(str(control_info.get("windowIcon", "")), group_box)

            btn_browse_wicon = QPushButton("Browse", group_box)
            btn_browse_wicon.setMinimumWidth(70)
            btn_browse_wicon.setMinimumHeight(20)  # Optional: Increase Browse button height
            layout.addWidget(lbl_wicon, row, 0)
            layout.addWidget(windowicon_lineedit, row, 1)
            layout.addWidget(btn_browse_wicon, row, 2)
            row += 1

            self.browse_buttons[btn_browse_wicon] = (control_name, "windowIcon_lineedit")
            btn_browse_wicon.clicked.connect(self.on_browse_file)

        # Save references to edit widgets
        self.edit_controls[control_name] = {
            "enabled_checkbox": enabled_checkbox,
            "type_lineedit": type_lineedit,
            "text_lineedit": text_lineedit,
            "icon_lineedit": icon_lineedit,
            "background_lineedit": background_lineedit,
            "windowIcon_lineedit": windowicon_lineedit,
        }

        return group_box

    def on_browse_file(self) -> None:
        """
        Unified slot function: Finds the corresponding lineEdit based on sender()
        and updates its text with the selected file path. Validates that the selected
        file is a PNG. If not, displays a warning message.
        """
        btn = self.sender()
        if btn not in self.browse_buttons:
            return

        control_name, lineedit_key = self.browse_buttons[btn]
        line_edit: Optional[QLineEdit] = self.edit_controls[control_name].get(lineedit_key)
        if not line_edit:
            return

        # Open file dialog allowing all file types
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*.*)")
        if file_path:
            # Check if the selected file has a .png extension (case-insensitive)
            if not file_path.lower().endswith('.png'):
                QMessageBox.warning(
                    self,
                    "Invalid File Type",
                    "The selected file type may be invalid. Please select a PNG file."
                )
                return  # Do not set the text if the file is invalid
            line_edit.setText(file_path)

    def save_and_close(self) -> None:
        """
        Write the edited information back to the YAML file (preserving comments,
        order, and uppercase True/False), then close the dialog.
        """
        for control_name, widgets_dict in self.edit_controls.items():
            # If the control_name is not in the original YAML, create an empty dict
            if control_name not in self.config_data:
                self.config_data[control_name] = {}

            # enabled
            self.config_data[control_name]["enabled"] = widgets_dict["enabled_checkbox"].isChecked()

            # type
            if widgets_dict["type_lineedit"] is not None:
                self.config_data[control_name]["type"] = widgets_dict["type_lineedit"].text()

            # text
            if widgets_dict["text_lineedit"] is not None:
                self.config_data[control_name]["text"] = widgets_dict["text_lineedit"].text()

            # icon
            if widgets_dict["icon_lineedit"] is not None:
                self.config_data[control_name]["icon"] = widgets_dict["icon_lineedit"].text()

            # background
            if widgets_dict["background_lineedit"] is not None:
                self.config_data[control_name]["background"] = widgets_dict["background_lineedit"].text()

            # windowIcon
            if widgets_dict["windowIcon_lineedit"] is not None:
                self.config_data[control_name]["windowIcon"] = widgets_dict["windowIcon_lineedit"].text()

        # Write back to the YAML file
        with open(self.yaml_path, 'w', encoding='utf-8') as f:
            self.yaml_parser.dump(self.config_data, f)

        self.accept()  # Close the dialog


class IMConfigDialog(QDialog):
    def __init__(self, yaml_path: str, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the IMConfigDialog.

        Args:
            yaml_path (str): Path to the YAML configuration file.
            parent (Optional[QWidget]): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.setWindowTitle("Configuration Settings")
        self.yaml_path = yaml_path
        self.yaml = YAML()
        self.yaml.preserve_quotes = True  # Preserve quotes in YAML

        # Global setting for flow_style
        # Set to True to use flow style, i.e., using brackets and commas
        # Set to False to use block style, i.e., each element on a separate line
        self.yaml.default_flow_style = False  # Modify to True or False as needed

        # Set the initial size of the dialog
        self.resize(600, 600)  # Increase width and height as needed

        self.config_data: Optional[CommentedMap] = None
        self.widgets: Dict[str, Dict[str, Any]] = {}  # Store widgets for each config key

        # Load YAML configuration
        try:
            self.load_yaml()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load configuration file: {e}")
            self.reject()
            return

        # Initialize UI
        self.init_ui()

    def load_yaml(self) -> None:
        """
        Load the YAML configuration file.

        Raises:
            FileNotFoundError: If the YAML file does not exist.
            TypeError: If the YAML root element is not a dictionary.
        """
        if not os.path.isfile(self.yaml_path):
            raise FileNotFoundError(f"Configuration file does not exist: {self.yaml_path}")
        with open(self.yaml_path, 'r', encoding='utf-8') as f:
            self.config_data = self.yaml.load(f)

        if not isinstance(self.config_data, CommentedMap):
            raise TypeError("Configuration file format error: Root element must be a dictionary")

    def init_ui(self) -> None:
        """
        Initialize the user interface by creating widgets based on YAML content.
        """
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)  # Set overall margins
        main_layout.setSpacing(10)  # Set overall spacing

        # Create a scroll area to accommodate many settings
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(10, 10, 10, 10)  # Set margins inside the scroll area
        scroll_layout.setSpacing(10)  # Set spacing inside the scroll area

        # Iterate through each top-level key in YAML
        for section, settings in self.config_data.items():
            group_box = QGroupBox(section)
            group_layout = QGridLayout()
            group_layout.setContentsMargins(10, 10, 10, 10)  # Set margins for the group box
            group_layout.setSpacing(10)  # Set spacing for the group box

            if isinstance(settings, dict):
                row = 0
                for key, value in settings.items():
                    label = QLabel(key)
                    widget = self.create_widget(section, key, value)
                    if widget:
                        group_layout.addWidget(label, row, 0, alignment=Qt.AlignLeft)
                        group_layout.addWidget(widget['widget'], row, 1)
                        if 'button' in widget:
                            group_layout.addWidget(widget['button'], row, 2)
                        self.widgets[f"{section}.{key}"] = widget
                        row += 1
            else:
                QMessageBox.warning(self, "Warning", f"Skipping unsupported section: {section}")
                continue

            group_box.setLayout(group_layout)
            scroll_layout.addWidget(group_box)

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # Add Confirm and Cancel buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        confirm_btn = QPushButton("Confirm")
        confirm_btn.setMinimumWidth(80)
        confirm_btn.setMinimumHeight(25)  # Increased height

        confirm_btn.clicked.connect(self.save_config)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumWidth(80)
        cancel_btn.setMinimumHeight(25)  # Increased height
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(confirm_btn)
        button_layout.addWidget(cancel_btn)

        main_layout.addLayout(button_layout)

    def create_widget(self, section: str, key: str, value: Any) -> Dict[str, Any]:
        """
        Create appropriate widget based on the value type and key.

        Args:
            section (str): The section name in YAML.
            key (str): The configuration key.
            value (Any): The configuration value.

        Returns:
            Dict[str, Any]: A dictionary containing 'widget' and optionally 'button'.
        """
        widget_info: Dict[str, Any] = {}
        if isinstance(value, str):
            # Determine if the key relates to a file path
            if 'path' in key.lower() or 'dir' in key.lower() or 'file' in key.lower():
                line_edit = QLineEdit(value)
                browse_btn = QPushButton("Browse")
                browse_btn.setMinimumWidth(70)
                browse_btn.setMinimumHeight(20)  # Optional: Increase Browse button height
                browse_btn.setObjectName(f"{section}.{key}")
                browse_btn.clicked.connect(self.browse_file_or_dir)
                widget_info['widget'] = line_edit
                widget_info['button'] = browse_btn
            else:
                # Regular text field
                line_edit = QLineEdit(value)
                widget_info['widget'] = line_edit

        elif isinstance(value, int):
            spin_box = QSpinBox()
            spin_box.setMaximum(1000000)  # Adjust as needed
            spin_box.setValue(value)
            widget_info['widget'] = spin_box

        elif isinstance(value, float):
            double_spin = QDoubleSpinBox()
            double_spin.setMaximum(1000000.0)  # Adjust as needed
            double_spin.setDecimals(4)
            double_spin.setValue(value)
            widget_info['widget'] = double_spin

        elif isinstance(value, list):
            # For lists, especially lists of integers (e.g., camera_number)
            if all(isinstance(item, int) for item in value):
                line_edit = QLineEdit(','.join(map(str, value)))
                widget_info['widget'] = line_edit
                # Removed individual list flow_style handling
                # Because we are now using the global setting
            else:
                # Handle other list types if necessary
                line_edit = QLineEdit(str(value))
                widget_info['widget'] = line_edit

        else:
            # Fallback to a disabled QLineEdit for unsupported types
            line_edit = QLineEdit(str(value))
            line_edit.setEnabled(False)
            widget_info['widget'] = line_edit

        return widget_info

    def browse_file_or_dir(self) -> None:
        """
        Open a file or directory dialog based on the button's associated key.
        """
        sender = self.sender()
        if not isinstance(sender, QPushButton):
            return

        object_name = sender.objectName()
        if '.' not in object_name:
            QMessageBox.warning(self, "Warning", "Invalid object name for browsing.")
            return

        section, key = object_name.split('.', 1)
        widget_info = self.widgets.get(f"{section}.{key}", {})
        line_edit: QLineEdit = widget_info.get('widget')

        if not isinstance(line_edit, QLineEdit):
            QMessageBox.warning(self, "Warning", "Associated widget is not a QLineEdit.")
            return

        current_value = line_edit.text()
        if 'dir' in key.lower():
            selected = QFileDialog.getExistingDirectory(self, "Select Directory", current_value)
        else:
            selected, _ = QFileDialog.getOpenFileName(self, "Select File", current_value)

        if selected:
            line_edit.setText(selected)

    def save_config(self) -> None:
        """
        Save the modified configuration back to the YAML file.
        """
        if not self.config_data:
            QMessageBox.critical(self, "Error", "Configuration data is empty. Cannot save.")
            return

        # Update config_data with widget values
        for full_key, widget_info in self.widgets.items():
            section, key = full_key.split('.', 1)
            widget = widget_info['widget']
            original_value = self.config_data[section][key]

            # Determine the type and retrieve the value accordingly
            if isinstance(original_value, str):
                new_value = widget.text()
            elif isinstance(original_value, int):
                new_value = widget.value()
            elif isinstance(original_value, float):
                new_value = widget.value()
            elif isinstance(original_value, list):
                text = widget.text()
                try:
                    # Attempt to parse as comma-separated integers
                    new_value = [int(item.strip()) for item in text.split(',') if item.strip().isdigit()]
                except ValueError:
                    QMessageBox.warning(self, "Warning", f"Invalid list format: {full_key}")
                    return

                # Use global flow_style setting
                list_seq = self.config_data[section][key]
                if isinstance(list_seq, CommentedSeq):
                    list_seq.clear()
                    list_seq.extend(new_value)
                else:
                    QMessageBox.warning(self, "Warning", f"The key {full_key} is not a CommentedSeq.")
                    return

            else:
                # Unsupported type, skip
                continue

            self.config_data[section][key] = new_value

        # Write back to YAML file
        try:
            with open(self.yaml_path, 'w', encoding='utf-8') as f:
                self.yaml.dump(self.config_data, f)
            QMessageBox.information(self, "Success", "Please restart the app!\n"
                                                     "The new configuration will take effect next time.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save configuration file: {e}")
