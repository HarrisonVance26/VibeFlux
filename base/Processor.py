from PySide6.QtCore import QObject, Signal, QTimer


class IMediaSignals(QObject):
    """
    The MediaSignals class encapsulates signals related to media operations.

    Attributes:
        frameReady (Signal): Signal emitted when a new frame is ready.
        mediaOpened (Signal): Signal emitted when the media feed is successfully opened.
        mediaClosed (Signal): Signal emitted when the media feed is closed.
        mediaFailed (Signal): Signal emitted when opening the media feed fails, sending the error message as a string.
        stopOtherActivities (Signal): Signal emitted when the media feed starts, indicating that other activities
        should be stopped.
    """
    frameReady = Signal(object)
    mediaOpened = Signal()
    mediaClosed = Signal()
    mediaFailed = Signal(str)
    stopOtherActivities = Signal()

    def __init__(self, device=0, fps=30, parent=None):
        """
        Initializes the MediaHandler object.

        :param device: The camera device number or the path to a video file. Default is 0, which usually refers to the
                       primary camera.
        :param fps: Frames per second for the media playback. Default is 30.
        :param parent: The parent QObject. Default is None.
        """
        super().__init__(parent)
        # Device could be an integer representing the camera number or a string representing a video file path.
        self.device = device
        self.fps = fps  # The frames per second of the media.
        self.frame_processors = []  # List of frame processing functions.
        self.timer_media = QTimer()  # Timer for capturing frames at regular intervals.
        # Connect the timer's timeout signal to the frame grabbing function.
        self.timer_media.timeout.connect(self._grabFrame)

    def addFrameProcessor(self, func):
        """
        Adds a frame processing function to the list. This function will be applied to each frame of the media.

        :param func: A function that takes an image as input and returns a processed image.
        """
        self.frame_processors.append(func)

    def removeFrameProcessor(self, func):
        """
        Removes a frame processing function from the list.

        :param func: The function to remove from the frame processing list.
        """
        self.frame_processors.remove(func)

    def setDevice(self, device):
        """
        Sets the media source device.

        :param device: The new camera device index or video file path to set.
        """

        self.device = device

    def _grabFrame(self):
        """
        Internal method called by the timer to grab and process frames from the media feed.
        Emits a signal with the processed frame.
        """
        pass

    def isActive(self):
        """
        Checks if the media feed is currently active (playing).

        :return: True if the media feed is active, False otherwise.
        """
        return self.timer_media.isActive()


class ImageSignals(QObject):
    """
    ImageHandler is responsible for managing and processing image files. It provides functionalities to process images
    individually or in batches if provided with a directory path. The class supports custom image processing
    functionalities, where each image can be processed using user-defined functions. Signals are emitted to indicate
    the progress and results of the image processing tasks.
    """
    frameReady = Signal(object)  # Signal emitted when an image has been processed. It carries the processed image.
    imageOpened = Signal()  # Signal emitted when an image processing task starts.
    imageClosed = Signal()  # Signal emitted when an image processing task ends.

    # Signal emitted when an error occurs during image processing. It carries an error message.
    imageFailed = Signal(str)

    # Signal emitted before starting an image processing task.
    # It can be used to stop other activities that could interfere with the image processing.
    stopOtherActivities = Signal()

    def __init__(self, parent=None):
        """
        Constructs an ImageHandler with an optional parent.
        :param parent: The parent QObject. Default is None.
        """
        super().__init__(parent)
        self.path = None  # Path of the image or directory to be processed.
        self.file_name = None  # Name of the current file being processed.
        self.frame_processors = []  # List of functions that will be applied to each image.
        self.processing = False  # Boolean flag indicating whether an image is currently being processed.

    def addFrameProcessor(self, func):
        """
        Adds a function to the list of image processors. Each processor is applied sequentially to the images.

        :param func: A callable function that takes an image as input and returns the processed image.
        """
        self.frame_processors.append(func)

    def removeFrameProcessor(self, func):
        """
        Removes a function from the list of processors that are applied to each image.

        :param func: The function to be removed from the processing list.
        """
        self.frame_processors.remove(func)

    def setPath(self, path):
        """
        Sets the path of the image or directory to be processed.

        :param path: The file or directory path to the image(s) to be processed.
        """
        self.path = path

    def stopProcess(self):
        """
        Stops the ongoing image processing tasks. Emits an 'imageClosed' signal after processing is stopped.
        """
        self.processing = False
        self.imageClosed.emit()

    def isActive(self):
        """
        Checks if the ImageHandler is currently processing an image.

        :return: True if an image is being processed, False otherwise.
        """
        return self.processing

    def getFileName(self):
        """
        Gets the name of the current file being processed.

        :return: The name of the current file.
        """
        return self.file_name
