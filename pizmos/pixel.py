from pygame import Surface, surfarray
from pygame import BLEND_ALPHA_SDL2, SRCALPHA
from numpy import array
from secrets import randbelow
from collections.abc import Sequence


def replace_color(surf: Surface, old: Sequence, new: Sequence) -> Surface:
    """
    replaces a color in an image, supports 24-bit and 32-bit formats.
    """
    if not isinstance(surf, Surface):
        raise TypeError
    elif surf.get_bitsize() not in [24, 32]:
        raise AttributeError(f"Surface: {surf} does not have a supported pixel format.")

    if len(old) > 3:
        old = old[:3]

    surf.lock()
    _pixels = surfarray.pixels3d(surf)

    for i in range(_pixels.shape[0]):
        for j in range(_pixels.shape[1]):
            _pixel: array = _pixels[i, j]
            if list(_pixel) == old:
                _replacement_pixel = array(new, dtype="uint8")
                _pixels[i, j] = _replacement_pixel
    del _pixels
    surf.unlock()
    return surf


def get_surfcolors(img: Surface) -> tuple:
    """
    Loop through a surface and grab the colors its made of
    sort from lightest(n) to darkest(0)
    """
    if not isinstance(img, Surface):
        raise TypeError

    _alpha: int = img.get_alpha()
    if _alpha == None:
        _alpha = 255

    excluded = []
    if _cc := img.get_colorkey():
        excluded.append(list(_cc))

    colors = list()
    pixel_color = list()
    for row in surfarray.array3d(img):
        for pixel in row:
            pixel_color = list(pixel)
            pixel_color.append(_alpha)
            if pixel_color not in excluded + colors:
                colors.append(pixel_color)

    colors.sort(key=sum)
    return tuple(colors)


def coloredsurf(size: tuple = (64, 64)) -> Surface:
    """
    Create a surface and fill each corner with a random color
    """
    _surf = Surface(size, flags=BLEND_ALPHA_SDL2 | SRCALPHA)
    _colors = [
        (randbelow(256), randbelow(256), randbelow(256), (255)) for _ in range(4)
    ]

    _cw, _ch = size[0] // 2, size[1] // 2
    for i in range(2):
        _surf.fill(_colors.pop(), (_cw * i, 0, _cw, _ch))
        _surf.fill(_colors.pop(), (_cw * i, _ch, _cw, _ch))
    return _surf
