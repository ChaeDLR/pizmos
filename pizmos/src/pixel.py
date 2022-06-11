import pygame


def replace_color(surf: pygame.Surface, old: tuple | list, new: tuple | list):
    """
    replace a color in an image
    use colorkey if old is none
    """
    if not isinstance(surf, pygame.Surface): raise TypeError
    for row in pygame.surfarray.array3d(surf):
        if row == old: row = new

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
