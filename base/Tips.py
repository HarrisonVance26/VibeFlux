from PySide6.QtCore import Qt, QTimer, QEasingCurve, Property, QPoint
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QGraphicsDropShadowEffect, QPushButton
from PySide6.QtCore import QPropertyAnimation


class IMTipWidget(QWidget):
    """
    A custom widget for displaying tooltip messages with fade-in and fade-out animations.

    This widget is designed to overlay on its parent widget and provide a non-intrusive notification message.
    """

    def __init__(self, parent: QWidget = None, font_family: str = "Arial", font_size: int = 20):
        """
        Initialize the TipWidget with default styles, animations, timers, and custom font settings.

        Args:
            parent (QWidget, optional): The parent widget for the tooltip. Defaults to None.
            font_family (str, optional): The font family for the tooltip text. Defaults to "Arial".
            font_size (int, optional): The font size for the tooltip text. Defaults to 20.

        Attributes:
            _opacity (float): Current opacity value of the widget (0.0 to 1.0).
            timer (QTimer): Timer for controlling the static display duration.
            animation (QPropertyAnimation): Animation object for fade-in and fade-out effects.
            _duration (int): Duration (in milliseconds) for which the tooltip remains visible.
        """
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self._opacity = 1.0  # Default opacity

        # Set up the basic style for the tooltip
        self.setStyleSheet(
            """
            QWidget {
                background-color: rgba(30,30,30,200);
                border-radius: 8px;
                border: 1px solid rgba(255,255,255,30);
                padding: 10px;
            }
            QLabel {
                color: #FFFFFF;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        # 设置字体
        self.label.setFont(QFont(font_family, font_size))
        layout.addWidget(self.label)

        # Timer for controlling the display duration
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.fadeOut)

        # Animation for fade-in and fade-out effects
        self.animation = QPropertyAnimation(self, b"opacity", self)
        self.animation.setDuration(500)  # Animation duration in milliseconds
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

        self._duration = 3000  # Default display duration in milliseconds

    def setOpacity(self, opacity: float) -> None:
        """
        Set the opacity of the tooltip.

        Args:
            opacity (float): A value between 0.0 (fully transparent) and 1.0 (fully opaque).
        """
        self._opacity = opacity
        self.setWindowOpacity(opacity)

    def getOpacity(self) -> float:
        """
        Retrieve the current opacity value of the tooltip.

        Returns:
            float: Current opacity value, ranging from 0.0 to 1.0.
        """
        return self._opacity

    opacity = Property(float, fget=getOpacity, fset=setOpacity)

    def showTip(self, text: str, duration: int = 3000, position: str | tuple[int, int] | QPoint = "center") -> None:
        """
        Display the tooltip with the specified text, duration, and position.

        Args:
            text (str): The message to display on the tooltip.
            duration (int, optional): The duration (in milliseconds) the tooltip should remain visible. Defaults to 3000.
            position (str | tuple[int, int] | QPoint, optional):
                The desired position of the tooltip. Options include:
                - "center": Center of the parent widget.
                - "top": Top of the parent widget.
                - "bottom": Bottom of the parent widget.
                - (x, y): Coordinates relative to the parent widget.
                - QPoint(x, y): QPoint object specifying the position.
        """
        # Stop and reset the animation and timer
        self.animation.stop()
        self.timer.stop()
        try:
            self.animation.finished.disconnect()
        except:
            pass

        self.setWindowOpacity(0.0)  # Start from fully transparent

        self._duration = duration
        self.label.setText(text)  # Set the tooltip text

        self.adjustSize()  # Adjust size to fit the text
        self.setPosition(position)  # Set position based on input

        self.fadeIn()  # Start fade-in animation
        self.show()

    def setPosition(self, position: str | tuple[int, int] | QPoint) -> None:
        """
        Set the position of the tooltip relative to its parent widget.

        Args:
            position (str | tuple[int, int] | QPoint):
                The desired position of the tooltip. Options include:
                - "center": Center of the parent widget.
                - "top": Top of the parent widget.
                - "bottom": Bottom of the parent widget.
                - (x, y): Coordinates relative to the parent widget.
                - QPoint(x, y): QPoint object specifying the position.
        """
        if self.parent() is None:
            return

        parent_rect = self.parent().geometry()

        if isinstance(position, str):
            x = parent_rect.x() + (parent_rect.width() - self.width()) // 2
            if position == "center":
                y = parent_rect.y() + (parent_rect.height() - self.height()) // 2
            elif position == "top":
                y = parent_rect.y() + 20
            elif position == "bottom":
                y = parent_rect.y() + parent_rect.height() - self.height() - 20
            else:
                y = parent_rect.y() + (parent_rect.height() - self.height()) // 2
            self.move(QPoint(x, y))

        elif isinstance(position, (tuple, list)) and len(position) == 2:
            x, y = position
            self.move(QPoint(x, y))

        elif isinstance(position, QPoint):
            self.move(position)

        else:
            x = parent_rect.x() + (parent_rect.width() - self.width()) // 2
            y = parent_rect.y() + (parent_rect.height() - self.height()) // 2
            self.move(QPoint(x, y))

    def fadeIn(self) -> None:
        """
        Start the fade-in animation to make the tooltip visible (opacity: 0.0 to 1.0).
        """
        self.animation.stop()
        try:
            self.animation.finished.disconnect()
        except:
            pass

        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setDuration(500)

        def on_fade_in_finished() -> None:
            """
            Triggered when the fade-in animation completes. Starts the display timer.
            """
            self.timer.start(self._duration)

        self.animation.finished.connect(on_fade_in_finished)
        self.animation.start()

    def fadeOut(self) -> None:
        """
        Start the fade-out animation to hide the tooltip (opacity: 1.0 to 0.0).
        """
        self.animation.stop()
        try:
            self.animation.finished.disconnect()
        except:
            pass

        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setDuration(500)

        def on_fade_out_finished() -> None:
            """
            Triggered when the fade-out animation completes. Hides the widget.
            """
            self.hide()

        self.animation.finished.connect(on_fade_out_finished)
        self.animation.start()

    def closeEvent(self, event) -> None:
        """
        Handle the close event by stopping the timer and performing cleanup.

        Args:
            event (QCloseEvent): The close event object.
        """
        self.timer.stop()
        super().closeEvent(event)
