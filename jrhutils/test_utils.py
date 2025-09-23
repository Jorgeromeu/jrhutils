from PIL import Image, ImageDraw, ImageFont
import matplotlib
from pathlib import Path
import matplotlib.colors as mcolors
from typing import Tuple, Union, Sequence

def get_default_font_path():
    font_path = str(Path(matplotlib.get_data_path()) / 'fonts/ttf/DejaVuSans.ttf')
    return font_path

ColorInput = Union[str, Sequence[float]]


def parse_color(color: ColorInput) -> Tuple[int, int, int]:
    """
    Normalize a color input to an (R, G, B) tuple of integers in [0, 255].

    Accepts:
    - named colors ("red", "blue", etc.)
    - hex strings ("#ff00ff", "#abc")
    - grayscale shorthand ("0.5")
    - RGB tuples/lists in [0,1] or [0,255]
    """
    if isinstance(color, str):
        rgb_float = mcolors.to_rgb(color)
        return tuple(int(c * 255) for c in rgb_float)

    if isinstance(color, Sequence):
        if len(color) == 3:
            # If values look like 0–255, return as integers
            if max(color) > 1:
                return tuple(int(c) for c in color)
            # If values are in [0,1], convert to [0,255]
            return tuple(int(c * 255) for c in color)
        elif len(color) == 4:
            # ignore alpha if passed
            vals = color[:3]
            if max(vals) > 1:
                return tuple(int(c) for c in vals)
            return tuple(int(c * 255) for c in vals)

    raise ValueError(f"Unsupported color format: {color!r}")

def test_img(
    txt: str = "",
    resolution=200,
    font_percent=0.3,
    color: ColorInput ="lightgray",
    textcolor: ColorInput ="white",
):
    
    color = parse_color(color)
    textcolor = parse_color(textcolor)

    image_size = (resolution, resolution)
    image = Image.new("RGB", image_size, color=color)  

    # Draw the text on the image
    draw = ImageDraw.Draw(image)
    font_size = resolution * font_percent

    font_path = get_default_font_path()    
    font = ImageFont.truetype(font_path, int(font_size))

    # # Get bounding box of the text
    bbox = draw.textbbox((0, 0), txt, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_position = (
        (image_size[0] - text_width) / 2,
        (image_size[1] - text_height) / 2,
    )

    draw.text(text_position, txt, fill=textcolor, font=font)

    return image

def checkerboard_img(
    resolution=100,
    num_squares=10,
    color1='white',
    color2='lightgray',
):
    color1 = parse_color(color1)
    color2 = parse_color(color2)

    size = (resolution, resolution)
    square_size = round(resolution / num_squares)
    print(square_size)

    width, height = size
    img = Image.new("RGB", size)
    pixels = img.load()

    for y in range(height):
        for x in range(width):
            # Determine if the square should be color1 or color2
            if ((x // square_size) + (y // square_size)) % 2 == 0:
                pixels[x, y] = color1
            else:
                pixels[x, y] = color2

    return img