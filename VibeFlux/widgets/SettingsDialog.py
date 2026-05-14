# VibeFlux, AGPL-3.0 license
import os
from typing import Dict, Any, Optional, Tuple

from PySide6.QtWidgets import QWidget, QGroupBox, QPushButton, QMessageBox, QDialog
from ..base.Widget import IMSettingsDialog, IMConfigDialog
from ..styles import BaseStyle


class SettingsDialog(IMSettingsDialog):
    def __init__(self, yaml_path: str, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the SettingsDialog.

        Args:
            yaml_path (str): Path to the YAML configuration file.
            parent (Optional[QWidget], optional): Parent widget. Defaults to None.
        """
        super().__init__(yaml_path, parent)

        # ===================== Style Enhancements =====================
        # Use QSS to beautify the dialog
        self.styles = BaseStyle()
        self.styles.set_named_style(self, style_name='LightStyle')

    def load_yaml(self, yaml_path: str) -> Dict[str, Any]:
        """
        Load YAML file using ruamel.yaml while preserving comments, order, and case.

        Args:
            yaml_path (str): Path to the YAML configuration file.

        Returns:
            Dict[str, Any]: Parsed YAML data.
        """
        return super().load_yaml(yaml_path)

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

        return super().create_control_group(control_name, control_info)

    def on_browse_file(self) -> None:
        """
        Unified slot function: Finds the corresponding lineEdit based on sender()
        and updates its text with the selected file path. Validates that the selected
        file is a PNG. If not, displays a warning message.
        """
        super().on_browse_file()

    def save_and_close(self) -> None:
        """
        Write the edited information back to the YAML file (preserving comments,
        order, and uppercase True/False), then close the dialog.
        """
        super().save_and_close()


class ConfigDialog(IMConfigDialog):
    def __init__(self, yaml_path: str, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the ConfigDialog by calling the parent class's initializer.

        Args:
            yaml_path (str): Path to the YAML configuration file.
            parent (Optional[QWidget]): Parent widget. Defaults to None.
        """
        super().__init__(yaml_path, parent)
        # Additional initialization for ConfigDialog can be added here if needed
        self.styles = BaseStyle()
        self.styles.set_named_style(self, style_name='LightStyle')

    def load_yaml(self) -> None:
        """
        Load the YAML configuration file using the parent class's method.
        """
        super().load_yaml()
        # Additional processing after loading YAML can be added here if needed

    def init_ui(self) -> None:
        """
        Initialize the user interface by creating widgets based on YAML content.
        Utilizes the parent class's method.
        """
        super().init_ui()
        # Additional UI setup specific to ConfigDialog can be added here if needed

    def create_widget(self, section: str, key: str, value: Any) -> Dict[str, Any]:
        """
        Create appropriate widget based on the value type and key.
        Utilizes the parent class's method.

        Args:
            section (str): The section name in YAML.
            key (str): The configuration key.
            value (Any): The configuration value.

        Returns:
            Dict[str, Any]: A dictionary containing 'widget' and optionally 'button'.
        """
        widget_info = super().create_widget(section, key, value)
        # Modify widget_info if necessary for ConfigDialog
        return widget_info

    def browse_file_or_dir(self) -> None:
        """
        Open a file or directory dialog based on the button's associated key.
        Utilizes the parent class's method.
        """
        super().browse_file_or_dir()
        # Additional functionality after browsing can be added here if needed

    def save_config(self) -> None:
        """
        Save the modified configuration back to the YAML file.
        Utilizes the parent class's method.
        """
        super().save_config()
        # Additional actions after saving config can be added here if needed
