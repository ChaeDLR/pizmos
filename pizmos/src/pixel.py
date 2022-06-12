import pygame

from numpy import array


def replace_color(surf: pygame.Surface, old: tuple | list, new: tuple | list) -> pygame.Surface:
    """
    replaces a color in an image, supports 24-bit and 32-bit formats.
    """
    if not isinstance(surf, pygame.Surface):
        raise TypeError
    elif surf.get_bitsize() not in [24, 32]:
        raise AttributeError(f"Surface: {surf} does not have a supported pixel format.")

    if len(old) > 3:
        old = old[:3]

    surf.lock()
    _pixels = pygame.surfarray.pixels3d(surf)

    for i in range(_pixels.shape[0]):
        for j in range(_pixels.shape[1]):
            _pixel: array = _pixels[i, j]
            if list(_pixel) == old:
                _replacement_pixel = array(new, dtype="uint8")
                _pixels[i, j] = _replacement_pixel
    del _pixels
    surf.unlock()
    return surf

def get_surfcolors(img: pygame.Surface) -> tuple:
    """
    Loop through a surface and grab the colors its made of
    sort from lightest(n) to darkest(0)
    """
    if not isinstance(img, pygame.Surface): raise TypeError

    _alpha: int = img.get_alpha()
    if _alpha == None:
        _alpha = 255
    
    excluded = []
    if _cc := img.get_colorkey():
        excluded.append(list(_cc))

    colors = list()
    pixel_color = list()
    for row in pygame.surfarray.array3d(img):
        for pixel in row:
            pixel_color = list(pixel)
            pixel_color.append(_alpha)
            if pixel_color not in excluded + colors:
                colors.append(pixel_color)

    colors.sort(key=sum)
    return tuple(colors)
