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
        excluded = [
                [255, 255, 255, 255],
                [0, 0, 0, 255],
            ]

        try:
            if _cc := img.get_colorkey(): excluded.append(list(_cc))
        except AttributeError:
            raise TypeError

        colors = list()
        pixel_color = list()
        for row in pygame.surfarray.array3d(img):
            for pixel in row:
                pixel_color = [int(pixel[0]), int(pixel[1]), int(pixel[2]), 255]
                if pixel_color not in excluded + colors:
                    colors.append(pixel_color)
        colors.sort(key=sum)
        return tuple(colors)
