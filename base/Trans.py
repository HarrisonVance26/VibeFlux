from PySide6 import QtGui, QtCore


def ToQtPixmap(cv_image_rgb):
    """
    Converts an RGB OpenCV image to a QPixmap.

    Args:
        cv_image_rgb (numpy.ndarray): The RGB OpenCV image to be converted.

    Returns:
        QPixmap: Converted QPixmap.
    """
    height, width, channel = cv_image_rgb.shape
    bytesPerLine = 3 * width
    qt_image = QtGui.QImage(cv_image_rgb.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
    return QtGui.QPixmap.fromImage(qt_image)


def scalePixmap(pixmap, size, keepAspect):
    """
    Scales a QPixmap to a specified size.

    :param pixmap: The QPixmap to be scaled.
    :param size: The QSize to scale the QPixmap to.
    :param keepAspect: Boolean indicating whether to keep the QPixmap's aspect ratio.
    :return: Scaled QPixmap.
    """
    aspectMode = QtCore.Qt.KeepAspectRatio if keepAspect else QtCore.Qt.IgnoreAspectRatio
    return pixmap.scaled(size, aspectMode, QtCore.Qt.SmoothTransformation)


def setPixmap(label, pixmap):
    """
    Set a QPixmap to a specified QLabel.
    :param label: The QLabel name.
    :param pixmap: The QPixmap to be scaled.
    """
    label.setPixmap(pixmap)
    label.setScaledContents(True)
