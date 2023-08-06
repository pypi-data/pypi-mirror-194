from PIL.Image import Image
from typing import Tuple, Union

MarginColor = Union[Tuple[int, int, int], Tuple[int, int, int, int]]


def _are_similar(color1, color2, max_diff):
    return all(map(
        lambda channel1, channel2: abs(channel1 - channel2) <= max_diff,
        color1,
        color2,
    ))


class ContentNotFound(Exception):
    pass


def crop_margins(image: Image, margin_color: MarginColor, max_margin_color_difference: int):
    image_data = image.getdata()

    def pixels():
        content_pixels = (
            (x, y)
            for x in range(image.width)
            for y in range(image.height)
            if not _are_similar(image_data[x+y*image.width], margin_color, max_margin_color_difference)
        )
        return content_pixels

    try:
        rect = (
            min(x for x, _y in pixels()),
            min(y for _x, y in pixels()),
            min(max(x for x, _y in pixels()) + 1, image.width),
            min(max(y for _x, y in pixels()) + 1, image.height)
        )
    except ValueError:
        raise ContentNotFound
    else:
        return image.crop(rect)
