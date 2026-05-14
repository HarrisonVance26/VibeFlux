from PySide6 import QtCore, QtGui
from PySide6.QtCore import QPoint, Qt, QRect
from PySide6.QtGui import QPainter, QCursor, QIcon
from PySide6.QtWidgets import QLabel, QDialog, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton


class IMageLabel(QLabel):
    """
    A QLabel extension that provides additional functionality for displaying images.

    This class extends QLabel, providing the ability to display images and text. It allows for interactive
    manipulation of the image being displayed. This includes the ability to scale the image in and out using the mouse
    wheel (zooming), as well as panning the image by clicking and dragging with the mouse.

    The class also provides a set of buttons for image scaling: resetting to the original size, and increasing or
    decreasing the size by 10%.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the FImageLabel instance.

        :param parent: The parent widget to the label. Default is None.
        """
        super(IMageLabel, self).__init__(*args, **kwargs)
        # Initialize variables
        self.__image = None  # Holds the image to be displayed in the label
        self.__scaled_img = None  # Holds the scaled version of the image
        self.__text = None  # Holds the text to be displayed in the label

        self.aspectMode = QtCore.Qt.KeepAspectRatio  # Sets the default aspect ratio mode
        self.keepAspect = True  # Flag indicating whether to keep the aspect ratio

        self.__point = None  # Holds the point where the image or text is to be drawn
        self.__start_pos = None  # Holds the starting position for drawing
        self.__end_pos = None  # Holds the ending position for drawing
        self.__left_click = False  # Flag indicating whether the left mouse button is clicked
        self.__scale = 1  # The scale factor for the image

        # Initialize font settings
        self.__font = QtGui.QFont()  # Create a QFont object
        self.__font.setFamily("楷体")  # Set the font family
        self.__font.setPointSize(16)  # Set the font size
        self.__painter = QPainter()  # Create a QPainter object

    def setAspectMode(self, keepAspect: bool):
        """
        Sets the aspect ratio mode for the label.

        :param keepAspect: If True, the aspect ratio is maintained.
        """
        if keepAspect:
            self.aspectMode = QtCore.Qt.KeepAspectRatio
        else:
            self.aspectMode = QtCore.Qt.IgnoreAspectRatio

    def dispText(self, text):
        """
        Displays text in the label.

        :param text: The text to display.
        """

        self.__text = text
        self.update()

    def dispImage(self, image, keepAspect=True):
        """
        Displays an image read by OpenCV in the label.

        :param image: The image to display.
        :param keepAspect: If True, the aspect ratio of the image is maintained.
        """

        if keepAspect:
            self.aspectMode = QtCore.Qt.KeepAspectRatio
        else:
            self.aspectMode = QtCore.Qt.IgnoreAspectRatio

        height, width, channel = image.shape  # Get the shape of the image
        bytesPerLine = 3 * width  # Calculate the number of bytes per line
        showImage = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                                 bytesPerLine, QtGui.QImage.Format_RGB888)  # Create a QImage from the image data
        pixmap = QtGui.QPixmap.fromImage(showImage)  # Create a QPixmap from the QImage
        self.__image = pixmap

        self.__image = self.__image.scaled(self.size(), self.aspectMode,
                                           QtCore.Qt.SmoothTransformation)  # Scale the image

        self.update()  # Update the label

    def paintEvent(self, e):
        """
        Handles paint events.

        :param e: The paint event.
        """
        painter = QPainter(self)  # Create a QPainter object

        if self.__image:  # If an image is set
            self.__scaled_img = self.__image.scaled(self.__image.size() * self.__scale, self.aspectMode,
                                                    QtCore.Qt.SmoothTransformation)  # Scale the image
            if not self.__point:  # If no point is set
                self.__point = QPoint((self.width() - self.__image.width()) / 2,
                                      (self.height() - self.__image.height()) / 2)  # Set the point

            painter.drawPixmap(self.__point, self.__scaled_img)  # Draw the image

        if self.__text:  # If text is set
            painter.setFont(self.__font)  # Set the font
            painter.setPen(Qt.blue)  # Set the pen color to blue
            painter.drawText(QRect(0, 0, self.geometry().width(), self.geometry().height()),
                             Qt.AlignCenter, self.__text)  # Draw the text

        painter.end()  # End the painter

    def wheelEvent(self, event):
        """
        Handles mouse wheel events. This will allow to zoom the image in or out.

        :param event: The wheel event.
        """

        if self.__image:  # If an image is set
            angle = event.angleDelta() / 8  # Get the angle at which the wheel is turned. The unit is 1/8 degrees
            angleY = angle.y()  # Get the y component of the angle

            if angleY > 0:  # If the wheel is scrolled up
                self.__scale *= 1.1  # Zoom in
            else:  # If the wheel is scrolled down
                self.__scale *= 0.9  # Zoom out

            self.update()  # Update the label

    def mouseMoveEvent(self, e):
        """
        Handles mouse move events. This will allow to pan the image when the mouse is moved.

        :param e: The mouse event.
        """
        if self.__image:  # If an image is set
            if self.__left_click:  # If the left mouse button is clicked
                self.__end_pos = e.pos() - self.__start_pos  # Get the current mouse position
                if not self.__point:  # If no point is set
                    self.__point = QPoint((self.width() - self.__image.width()) / 2,
                                          (self.height() - self.__image.height()) / 2)  # Set the point
                self.__point = self.__point + self.__end_pos  # Update the point
                # Set the current mouse position as the starting position for the next mouse move event
                self.__start_pos = e.pos()
                self.repaint()  # Redraw the image

    def mousePressEvent(self, e):
        """
        Handles mouse press events. This will start the panning operation.

        :param e: The mouse event.
        """
        if self.__image:  # If an image is set
            self.setCursor(QCursor(Qt.OpenHandCursor))  # Set the cursor to a hand cursor
            if e.button() == Qt.LeftButton:  # If the left mouse button is clicked
                self.__left_click = True  # Set the flag indicating that the left mouse button is clicked
                self.__start_pos = e.pos()  # Set the current mouse position as the starting position

    def mouseReleaseEvent(self, e):
        """
        Handles mouse release events. This will end the panning operation.

        :param e: The mouse event.
        """
        if self.__image:  # If an image is set
            self.setCursor(QCursor(Qt.ArrowCursor))  # Set the cursor back to an arrow cursor
            if e.button() == Qt.LeftButton:  # If the left mouse button is released
                self.__left_click = False  # Reset the flag indicating that the left mouse button is clicked

    def normButton(self):
        """
        Resets the image size to the original size.
        """
        if self.__image:  # If an image is set
            self.__scale = 1  # Reset the scale factor to 1

            self.__point = QPoint((self.width() - self.__image.width()) / 2,
                                  (self.height() - self.__image.height()) / 2)  # Set the point

            self.__image = self.__image.scaled(self.size(), self.aspectMode,
                                               QtCore.Qt.SmoothTransformation)  # Scale the image
            self.update()  # Update the label

    def bigButton(self):
        """
        Increases the size of the image by 10%.
        """
        if self.__image:  # If an image is set
            self.__scale *= 1.1  # Increase the scale factor by 10%
            self.update()  # Update the label

    def smallButton(self):
        """
        Decreases the size of the image by 10%.
        """
        if self.__image:  # If an image is set
            self.__scale *= 0.9  # Decrease the scale factor by 10%
            self.update()  # Update the label


class IMessageBox(QDialog):
    """
    This class represents a custom message box that inherits from QDialog.
    The message box includes a title, a message, and Yes/No buttons.
    """

    def __init__(self, *args, **kwargs):
        super(IMessageBox, self).__init__(*args, **kwargs)
        self.no_button = None
        self.yes_button = None
        self.message = None

    def set_icon(self, icon_path):
        """
        Sets the window icon.

        :param icon_path: The path to the icon file.
        """
        self.setWindowIcon(QIcon(icon_path))

    def layoutMessage(self, message="", yes_text="Yes", no_text="No"):
        # Create QLabel for the message and align the text to the center
        self.message = QLabel(message)
        self.message.setAlignment(Qt.AlignCenter)

        # Create the Yes and No buttons
        self.yes_button = QPushButton(yes_text)
        self.no_button = QPushButton(no_text)

        # Set the minimum and maximum size for the message and buttons
        self.message.setMinimumSize(300, 80)
        self.message.setMaximumSize(300, 80)
        self.yes_button.setMinimumSize(100, 40)
        self.yes_button.setMaximumSize(100, 50)
        self.no_button.setMinimumSize(100, 40)
        self.no_button.setMaximumSize(100, 50)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.yes_button)
        button_layout.addWidget(self.no_button)
        button_layout.setSpacing(50)  # Sets the spacing between the buttons

        # Create a vertical layout for the message and buttons
        layout = QVBoxLayout()
        layout.addWidget(self.message)
        layout.addLayout(button_layout)
        layout.setContentsMargins(30, 20, 30, 40)  # Sets the margins

        self.setLayout(layout)  # Sets the layout


class IMExtWindow(QMainWindow):
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
        super(IMExtWindow, self).__init__(*args, **kwargs)
