# VibeFlux, AGPL-3.0 license

import cv2


def find_cameras(max_devices: int = 3) -> list[int]:
    """
    Detects and returns a list of available camera device indices.

    Args:
        max_devices (int): The maximum number of devices to check. Defaults to 3.

    Returns:
        list[int]: A list of indices representing available camera devices.
    """
    available_cameras = []  # List to store indices of available cameras
    for device_index in range(max_devices):
        # Attempt to open the device using DirectShow backend
        cap = cv2.VideoCapture(device_index, cv2.CAP_DSHOW)
        if cap.isOpened():  # Check if the camera device is successfully opened
            ret, _ = cap.read()  # Try reading a frame to verify functionality
            if ret:  # If reading succeeds, add the device index to the list
                available_cameras.append(device_index)
            cap.release()  # Release the camera resource
    return available_cameras


def get_cam_resolutions(index: int) -> list[tuple[int, int]]:
    """
    Retrieves a list of resolutions supported by the specified camera.

    Args:
        index (int): The index of the camera device.

    Returns:
        list[tuple[int, int]]: A list of supported resolutions as (width, height) tuples.
    """
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print(f"Camera at index {index} could not be opened.")
        return []

    resolutions = []
    common_resolutions = [(1920, 1080), (1280, 720), (640, 480), (320, 240)]
    for width, height in common_resolutions:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if (actual_width, actual_height) == (width, height):
            resolutions.append((int(actual_width), int(actual_height)))

    cap.release()
    return resolutions


def set_cam_resolution(index: int, width: int, height: int) -> bool:
    """
    Sets the resolution of the specified camera.

    Args:
        index (int): The index of the camera device.
        width (int): Desired width.
        height (int): Desired height.

    Returns:
        bool: True if the resolution was successfully set, False otherwise.
    """
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print(f"Camera at index {index} could not be opened.")
        return False

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    cap.release()
    return (actual_width, actual_height) == (width, height)


def is_cam_available(index: int) -> bool:
    """
    Checks if a specific camera is available.

    Args:
        index (int): The index of the camera device.

    Returns:
        bool: True if the camera is available, False otherwise.
    """
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    available = cap.isOpened()
    cap.release()
    return available


def show_cam_feed(index: int) -> None:
    """
    Displays the real-time feed of the specified camera.

    Args:
        index (int): The index of the camera device.
    """
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print(f"Camera at index {index} could not be opened.")
        return

    print("Press 'q' to exit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting...")
            break
        cv2.imshow(f"Camera {index}", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def get_cam_properties(index: int) -> dict:
    """
    Retrieves various properties of the specified camera.

    Args:
        index (int): The index of the camera device.

    Returns:
        dict: A dictionary containing camera properties such as frame width, height, and FPS.
    """
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print(f"Camera at index {index} could not be opened.")
        return {}

    properties = {
        "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "fps": int(cap.get(cv2.CAP_PROP_FPS)),
        "fourcc": int(cap.get(cv2.CAP_PROP_FOURCC)),
    }

    cap.release()
    return properties
