# VibeFlux, AGPL-3.0 license
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from ..base.Tips import IMTipWidget


class MultiTipWidget(IMTipWidget):
    """
    An extended tooltip widget with multiple message types.

    Supports the following types: info, warning, error, success.
    Different types have unique color schemes and left-side indicators.
    """

    STYLES = {
        "info": """
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(255, 255, 255, 200),
                    stop: 1 rgba(245, 245, 245, 200)
                );
                border-radius: 8px;
                border: 1px solid rgba(0,0,0,0.1);
                border-left: 10px solid #2196F3; /* Blue stripe */
                padding: 10px;
            }
            QLabel {
                color: #333333;
                font-size: 20px;
                font-weight: 500;
            }
        """,
        "warning": """
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(255, 255, 255, 200),
                    stop: 1 rgba(245, 245, 245, 200)
                );
                border-radius: 8px;
                border: 1px solid rgba(0,0,0,0.1);
                border-left: 10px solid #FFC107; /* Yellow stripe */
                padding: 10px;
            }
            QLabel {
                color: #333333;
                font-size: 20px;
                font-weight: 500;
            }
        """,
        "error": """
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(255, 255, 255, 200),
                    stop: 1 rgba(245, 245, 245, 200)
                );
                border-radius: 8px;
                border: 1px solid rgba(0,0,0,0.1);
                border-left: 10px solid #F44336; /* Red stripe */
                padding: 10px;
            }
            QLabel {
                color: #333333;
                font-size: 20px;
                font-weight: 500;
            }
        """,
        "success": """
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(255, 255, 255, 200),
                    stop: 1 rgba(245, 245, 245, 200)
                );
                border-radius: 8px;
                border: 1px solid rgba(0,0,0,0.1);
                border-left: 10px solid #4CAF50; /* Green stripe */
                padding: 10px;
            }
            QLabel {
                color: #333333;
                font-size: 20px;
                font-weight: 500;
            }
        """
    }

    def __init__(self, parent=None, font_family: str = "Arial", font_size: int = 20):
        """
        Initialize the MultiTipWidget with default styles, effects, and custom font.

        Args:
            parent (QWidget, optional): The parent widget for the tooltip. Defaults to None.
            font_family (str, optional): The font family for the tooltip text. Defaults to "Arial".
            font_size (int, optional): The font size for the tooltip text. Defaults to 20.
        """
        super().__init__(parent, font_family, font_size)

        # Add a subtle drop shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(0, 2)
        shadow.setBlurRadius(8)
        shadow.setColor(Qt.gray)
        self.setGraphicsEffect(shadow)

        # Default style is info
        self.setStyleSheet(self.STYLES["info"])

    def showTip(self, text: str, duration: int = 3000, position="center", message_type="info") -> None:
        """
        Display the tooltip with the specified text, duration, position, and message type.

        Args:
            text (str): The message to display.
            duration (int, optional): The duration (in milliseconds) for which the tooltip remains visible. Defaults to 3000.
            position (str | tuple[int, int] | QPoint, optional): The position of the tooltip relative to its parent. Defaults to "center".
            message_type (str, optional): The message type (info, warning, error, success). Defaults to "info".
        """
        # Apply the style based on message type
        style = self.STYLES.get(message_type, self.STYLES["info"])
        self.setStyleSheet(style)

        # Call the parent method to handle positioning and fade-in
        super().showTip(text, duration, position)
