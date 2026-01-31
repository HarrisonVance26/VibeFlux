import random
import string

from PySide6.QtGui import QImage, QPixmap
from captcha.image import ImageCaptcha


def imRandCode(width=170, height=80, length=4, characters=None):
    """
    Generates a random verification code and returns an image of the code and the code itself as a string.

    :param width: The width of the image. Defaults to 170.
    :param height: The height of the image. Defaults to 80.
    :param length: The length of the verification code. Defaults to 4.
    :param characters: The set of characters to use for generating the code. Defaults to digits and uppercase ASCII letters.

    :return: Tuple of the image of the code and the code itself.
    """
    if characters is None:
        characters = string.digits + string.ascii_uppercase

    # Generate a random string of given length from the character set
    random_str = ''.join([random.choice(characters) for _ in range(length)])

    # Generate an image for the verification code
    generator = ImageCaptcha(width=width, height=height)
    img = generator.generate_image(random_str)

    # Convert the image to QPixmap
    im = img.convert("RGB")
    data = im.tobytes("raw", "RGB")
    bytesPerLine = 3 * im.size[0]
    qim = QImage(data, im.size[0], im.size[1], bytesPerLine, QImage.Format_RGB888)
    pix = QPixmap.fromImage(qim)

    return pix, random_str
