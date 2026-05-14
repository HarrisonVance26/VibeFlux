import random

from PIL import Image, ImageDraw, ImageFont, ImageQt


def imHBar(label_name, value, colors, width, height, value_name=None, color_text='#000000', alpha=0.8, margin=20,
           fontB=None):
    """
    Creates a horizontal bar chart image.

    Args:
        label_name (list): Labels for each bar.
        value (list): Values represented by each bar.
        colors (list): Color for each bar.
        width (int): Width of the output image.
        height (int): Height of the output image.
        value_name (list): Display values by each bar.
        color_text (str, optional): Color of the text. Defaults to black ('#000000').
        alpha (float, optional): Alpha value for the transparency of the bars. Defaults to 0.8.
        margin (int, optional): Margin between bars. Defaults to 20.
        fontB (ImageFont, optional): Font for the text. Defaults to None.

    Returns:
        QPixmap: An image of the bar chart.
    """
    if not value_name:
        # Ensure no division by zero
        max_value = max(value)
        # Calculate the height of each bar
        value_name = [(v / max_value) * (height - 50) for v in value]
    else:
        max_value = max(value_name)
        value_name = [(v / max_value) * (height - 50) for v in value_name]

    # Initialize the drawing area
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    num_bars = len(label_name)
    bar_width = (width - margin * num_bars - 10) / num_bars
    x1 = 10

    for i in range(num_bars):
        # Calculate the position and size of each bar
        x2 = x1 + bar_width
        y1 = height - 25 - value_name[i]  # Bottom of the bar
        y2 = height - 25  # Top of the bar

        # Draw each bar
        color = tuple(colors[i])
        rgba = (color[0], color[1], color[2], int(256 * alpha))
        draw.rectangle(((x1, y1), (x2, y2)), fill=rgba, outline=color, width=2)

        # Draw the label and value for each bar
        if not fontB:
            fontB = ImageFont.load_default()
        t_size = draw.textsize(label_name[i], fontB)
        label_bias = (bar_width - t_size[0]) / 2
        draw.text((x1 + label_bias, y2 + 5), label_name[i], fill=color_text, font=fontB)

        value_text = str(int(value[i]))
        t_size = draw.textsize(value_text, fontB)
        value_bias = (bar_width - t_size[0]) / 2
        draw.text((x1 + value_bias, y1 - t_size[1] - 5), value_text, fill=color_text, font=fontB)

        # Update the position for the next bar
        x1 += margin + bar_width

    # Convert the PIL image to a QPixmap
    pixmap = ImageQt.toqpixmap(img)
    return pixmap


def imVBar(label_name, value, colors, width, height, value_name=None, color_text='#000000',
           alpha=0.7, margin=20, fontB=None):
    """
    Creates a vertical bar chart image.

    Args:
        label_name (list): Labels for each bar.
        value (list): Values represented by each bar.
        colors (list): Color for each bar.
        width (int): Width of the output image.
        height (int): Height of the output image.
        value_name (list): Display values by each bar.
        color_text (str): Color of the text.
        alpha (float): Alpha value of the bars for transparency.
        margin (int): Margin between each bar.
        fontB (ImageFont, optional): Font for the text. Defaults to None.

    Returns:
        QPixmap: An image of the bar chart.
    """
    if not value_name:
        # Calculate the normalized value for each bar
        max_val = max(value)
        value_name = [v / max_val * (width - 50) for v in value]
    else:
        max_val = max(value_name)
        value_name = [v / max_val * (width - 50) for v in value_name]

    # Initialize the drawing area
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    num_bars = len(label_name)
    bar_height = (height - margin * num_bars - 10) / num_bars
    y1 = 10

    for i in range(num_bars):
        # Draw each bar
        x2 = 10 + value_name[i]
        y2 = y1 + bar_height
        color = tuple(colors[i])
        rgba = (color[0], color[1], color[2], int(256 * alpha))
        draw.rectangle(((10, y1), (x2, y2)), fill=rgba, outline=color, width=2)

        # Add text label and value
        if not fontB:
            fontB = ImageFont.load_default()
        label_size = draw.textsize(label_name[i], fontB)
        value_size = draw.textsize(str(int(value[i])), fontB)
        label_bias = (bar_height - label_size[1]) / 2
        value_bias = (bar_height - value_size[1]) / 2

        # Positioning the label and value text
        draw.text((10, y1 + label_bias), label_name[i], fill=color_text, font=fontB)
        text_x_pos = x2 + 5 if label_size[0] + 5 < x2 else 10 + label_size[0] + 5
        draw.text((text_x_pos, y1 + value_bias), str(int(value[i])), fill=color_text, font=fontB)

        # Update the position for the next bar
        y1 += margin + bar_height

    # Convert the PIL image to a QPixmap
    pixmap = ImageQt.toqpixmap(img)
    return pixmap


def imVBarPer(label_name, value, colors, width, height, value_name=None, color_text='#000000', alpha=0.7, margin=20,
              fontB=None):
    """
    Generate a vertical bar chart as a QPixmap.

    Args:
        label_name (list): List of bar labels.
        value (list): List of bar values.
        colors (list): List of RGB color tuples for each bar.
        width (int): The width of the generated chart image.
        height (int): The height of the generated chart image.
        value_name (list): Display values by each bar.
        color_text (str): The color of text.
        alpha (float): The alpha value (transparency) of the bars.
        margin (int): The margin between bars.
        fontB (ImageFont, optional): Font for the text. Defaults to None.

    Returns:
        QPixmap: QPixmap of the generated chart.
    """
    if not value_name:
        value_name = [v / max(value) * (width - 90) for v in value]
    else:
        value_name = [v / max(value_name) * (width - 90) for v in value_name]

    # Creating a new image with transparent background
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    num_bars = len(label_name)
    bar_height = (height - margin * num_bars - 10) / num_bars
    y1 = 10

    for i in range(num_bars):
        # Drawing the bar
        x2 = value_name[i] + 10
        y2 = y1 + bar_height
        color = tuple(colors[i])
        rgba = (color[0], color[1], color[2], int(256 * alpha))
        draw.rectangle(((10, y1), (x2, y2)), fill=rgba, outline=color, width=2)

        # Drawing the bar label and value label
        if not fontB:
            fontB = ImageFont.load_default()
        label_size = draw.textsize(label_name[i], fontB)
        value_text = f'{value[i]:.2f}%'
        value_size = draw.textsize(value_text, fontB)
        label_bias = (bar_height - label_size[1]) / 2
        value_bias = (bar_height - value_size[1]) / 2

        draw.text((10, y1 + label_bias), label_name[i], fill=color_text, font=fontB)
        text_x_pos = x2 + 5 if label_size[0] + 5 < x2 else 10 + label_size[0] + 5
        draw.text((text_x_pos, y1 + value_bias), value_text, fill=color_text, font=fontB)

        # Update the position for the next bar
        y1 += margin + bar_height

    # Convert image to QPixmap for display in a PyQt application
    pixmap = ImageQt.toqpixmap(img)
    return pixmap


def imRectBox(img, rect, color=None, alpha=0.25, addText=None, line_thickness=None, fontC=None):
    """
    Draws a rectangular bounding box on an image.

    Args:
        img (Image/): A PIL Image object representing the image to draw on.
        rect (list/tuple): 4 integers specifying the bounding box coordinates (x1, y1, x2, y2).
        color (list/tuple, optional): 3 integers specifying the color of the box (R, G, B). If None, a random color is used.
        alpha (float, optional): Alpha (transparency) of the box. Default is 0.25.
        addText (str, optional): Text to add to the box. If None, no text is added.
        line_thickness (int, optional): Thickness of the lines of the box. If None, calculated based on image dimensions.
        fontC (ImageFont, optional): Font object for the text. If None, default font is used.

    Returns:
        Image: A PIL Image object with the drawn box and text.
    """

    # Create a drawing context on the image
    draw = ImageDraw.Draw(img, "RGBA")

    # Calculate line thickness if not provided
    tl = line_thickness or round(0.002 * (img.width + img.height) / 2) + 1

    # If a specific color is not provided, generate a random one
    if color is not None:
        color = tuple(color)
    else:
        color = tuple([random.randint(0, 255) for _ in range(3)])

    # Get the corners of the rectangle
    c1, c2 = (int(rect[0]), int(rect[1])), (int(rect[2]), int(rect[3]))

    # Prepare the color with alpha for the rectangle fill
    rgba = (color[0], color[1], color[2], int(255 * alpha))

    # Draw the rectangle on the image
    draw.rectangle((c1, c2), fill=rgba, outline=color, width=tl)

    # If text is provided and a font object exists, add text on the box
    if addText and fontC:
        # Get the size of the text box
        t_size = draw.textsize(addText, fontC)
        # Position of the text box
        c1_text = c1[0], c1[1] - t_size[1] - 3
        c2_text = c1[0] + t_size[0] + 3, c1[1] - 3
        # Make sure the text box doesn't go outside the image
        if c1_text[1] < 0:
            c1_text = c1_text[0], 0
        if c2_text[1] < 0:
            c2_text = c2_text[0], 0

        # Draw the rectangle for the text
        draw.rectangle((c1_text, c2_text), fill=color, outline="#FF0000", width=0)
        # Draw the text
        draw.text((c1[0], c1_text[1]), addText, fill="#FFFFFF", font=fontC)

    # Return the final image (PIL Image object)
    return img


def imRectEdge(img, rect, color=None, alpha=0.2, addText=None, line_thickness=None, fontC=None):
    """
    Draw a rectangle with annotated edges on an image.

    Args:
        img (Image/): The PIL Image object to draw on.
        rect (tuple/list): The coordinates of the rectangle as (x1, y1, x2, y2).
        color (tuple/list, optional): The color of the rectangle as an RGB tuple. If None, a random color is used.
        alpha (float, optional): The alpha value (transparency) of the rectangle. Default is 0.2.
        addText (str, optional): Text to add to the rectangle.
        line_thickness (int, optional): The thickness of the rectangle's outline. Calculated based on image dimensions if None.
        fontC (ImageFont, optional): Font object for the text. If None, default font is used.

    Returns:
        Image: The modified PIL Image object.
    """

    draw = ImageDraw.Draw(img, "RGBA")

    # Calculate line thickness if not provided
    tl = line_thickness or round(0.002 * (img.width + img.height) / 2) + 1

    # Choose color
    if color is not None:
        color = tuple(color)
    else:
        color = tuple([random.randint(0, 255) for _ in range(3)])  # Random color if not provided

    c1, c2 = (int(rect[0]), int(rect[1])), (int(rect[2]), int(rect[3]))

    # Calculate rectangle dimensions
    w, h = c2[0] - c1[0], c2[1] - c1[1]
    len_edge = int(w / 10), int(h / 10)

    rgba = (color[0], color[1], color[2], int(256 * alpha))

    # Draw the rectangle
    draw.rectangle((c1, c2), fill=rgba, outline=color, width=0)

    # Draw rectangle corners
    draw.line([c1, (c1[0], c1[1] + len_edge[1])], fill=color, width=tl)
    draw.line([c1, (c1[0] + len_edge[0], c1[1])], fill=color, width=tl)
    draw.line([(c1[0] + w, c1[1]), (c2[0] - len_edge[0], c1[1])], fill=color, width=tl)
    draw.line([(c1[0] + w, c1[1]), (c2[0], c1[1] + len_edge[1])], fill=color, width=tl)
    draw.line([c2, (c2[0], c2[1] - len_edge[1])], fill=color, width=tl)
    draw.line([c2, (c2[0] - len_edge[0], c2[1])], fill=color, width=tl)
    draw.line([(c1[0], c2[1]), (c1[0], c2[1] - len_edge[1])], fill=color, width=tl)
    draw.line([(c1[0], c2[1]), (c1[0] + len_edge[0], c2[1])], fill=color, width=tl)

    # Add text if provided
    if addText and fontC:
        t_size = draw.textsize(addText, fontC)
        c1_text = c1[0], c1[1] - t_size[1] - 3
        c2_text = c1[0] + t_size[0] + 3, c1[1] - 3

        # Make sure the text box doesn't go outside the image
        if c1_text[1] < 0:
            c1_text = c1_text[0], 0
        if c2_text[1] < 0:
            c2_text = c2_text[0], 0

        draw.rectangle((c1_text, c2_text), fill=color, outline="#FF0000", width=0)
        draw.text((c1[0], c1_text[1]), addText, fill="#FFFFFF", font=fontC)

    # Return the modified PIL Image object
    return img


def draw_oriented_box(image, box, color=None, alpha=0.25, addText=None, line_thickness=None, fontC=None):
    """
    Draws an oriented bounding box (OBB) on an image.

    Args:
        image (PIL.Image.Image): A PIL Image object representing the image to draw on.
        box (list/tuple): 8 integers specifying the bounding box coordinates [x1, y1, x2, y2, x3, y3, x4, y4].
        color (list/tuple, optional): 3 integers specifying the color of the box (R, G, B). If None, a random color is used.
        alpha (float, optional): Alpha (transparency) of the box. Default is 0.25.
        addText (str, optional): Text to add to the box. If None, no text is added.
        line_thickness (int, optional): Thickness of the lines of the box. If None, calculated based on image dimensions.
        fontC (PIL.ImageFont.ImageFont, optional): Font object for the text. If None, default font is used.

    Returns:
        PIL.Image.Image: The image with the drawn OBB and text.
    """
    # Create a drawing context on the image
    draw = ImageDraw.Draw(image, "RGBA")

    # Calculate line thickness if not provided
    tl = line_thickness or round(0.002 * (image.width + image.height) / 2) + 1

    # If a specific color is not provided, generate a random one
    if color is not None:
        color = tuple(color)
    else:
        color = tuple([random.randint(0, 255) for _ in range(3)])

    # Prepare the color with alpha for the polygon fill
    rgba_fill = (color[0], color[1], color[2], int(255 * alpha))

    # Prepare the outline color (no alpha)
    outline_color = color

    # Convert box coordinates to integer and group into points
    pts = [(int(box[i]), int(box[i+1])) for i in range(0, len(box), 2)]

    # Draw the filled polygon
    draw.polygon(pts, fill=rgba_fill)

    # Draw the outline
    draw.line(pts + [pts[0]], fill=outline_color, width=tl)

    # If text is provided and a font object exists, add text on the box
    if addText:
        # Use default font if fontC is not provided
        if fontC is None:
            fontC = ImageFont.load_default()

        # Calculate the position to place the text (upper-left corner of the bounding box)
        x_coords = [point[0] for point in pts]
        y_coords = [point[1] for point in pts]
        x_min = min(x_coords)
        y_min = min(y_coords)

        # Measure text size
        text_size = draw.textsize(addText, font=fontC)

        # Adjust text position if it goes out of image bounds
        text_x = x_min
        text_y = y_min - text_size[1] - 3
        if text_x < 0:
            text_x = 0
        if text_y < 0:
            text_y = 0

        # Draw rectangle behind the text for better visibility
        text_background = (text_x, text_y, text_x + text_size[0] + 3, text_y + text_size[1] + 3)
        draw.rectangle(text_background, fill=color)

        # Draw the text
        draw.text((text_x + 1, text_y + 1), addText, fill="#FFFFFF", font=fontC)

    return image
