import pygame
import os


def get_image_at(
    rect: pygame.Rect | tuple[int, int, int, int],
    sheet: pygame.Surface,
    colorkey: tuple = None,
    scale: tuple = None,
) -> pygame.Surface:
    """Capture image from given file at the given rect.
    Optionally set transparancy colorkey and scale

    Args:
        rectangle (tuple): position, width, height of image
        filepath (str): image file path
        colorkey (tuple, optional): _description_. Defaults to None.
        scale (tuple, optional): _description_. Defaults to None.

    Returns:
        pygame.Surface: _description_
    """
    # Loads image from x, y, x+offset, y+offset
    if not isinstance(rect, pygame.Rect):
        rect = pygame.Rect(rect)
    image = pygame.Surface(rect.size).convert()
    image.blit(sheet, (0, 0), rect)
    if colorkey:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    if scale:
        return pygame.transform.scale(image, scale)
    return image


def get_subimages(sheet: pygame.Surface) -> list[pygame.Surface]:
    """Get subimages from a given surface using the given sheets transparancy colorkey.

    Args:
        sheet (pygame.Surface): Surface containing multiple images divided by a colorkey or the color at (0, 0)

    Returns:
        list[pygame.Surface]: A list containing all of the found subimages
    """
    _colorkey = sheet.get_colorkey()
    if _colorkey == None:
        _colorkey = sheet.get_at((0, 0))

    _colorkey = sheet.get_colorkey() if sheet.get_colorkey() else sheet.get_at((0, 0))
    _mask = pygame.mask.from_surface(sheet, threshold=174)
    _images = list()

    for surf, rect in [
        (
            pygame.Surface(
                _rect.size,
                flags=pygame.BLEND_ALPHA_SDL2 | pygame.SRCALPHA,
            ),
            _rect,
        )
        for _rect in _mask.get_bounding_rects()
    ]:
        surf.blit(sheet, (0, 0), area=rect)
        surf.set_colorkey(_colorkey)
        _images.append(surf)
    return _images


def trim(image: pygame.Surface) -> pygame.Surface:
    """Remove as much of the colorkey as possible

    Args:
        image (pygame.Surface)

    Returns:
        pygame.Surface
    """
    _img = image
    _mask: pygame.mask.Mask = pygame.mask.from_surface(_img)
    _rect: pygame.rect.Rect = _mask.get_bounding_rects()[0]
    image = pygame.Surface(_rect.size, flags=pygame.BLEND_ALPHA_SDL2)
    image.blit(_img, (0, 0), area=_rect)
    image.set_colorkey(image.get_at((0, 0)))
    return image


def cut_sheet(
    sheet: pygame.Surface, grid: tuple | list, margins: tuple | list = (0, 0, 0, 0)
) -> list[pygame.Surface]:
    """cut the spritesheet by the given dimensions

    Args:
        sheet (pygame.Surface)
        grid (Sequence[int, int]): number of (columns, rows) to slice
        margins (tuple, optional): [top, bottom, left, right]. Defaults to (0, 0, 0, 0).

    Returns:
        list[pygame.Surface]
    """
    img_width: int = int((sheet.get_width() - (margins[2] + margins[3])) / grid[0])
    img_height: int = int((sheet.get_height() - (margins[0] + margins[1])) / grid[1])

    cut_buttons = []
    for column in [int(img_width * i + margins[3]) for i in range(grid[0])]:
        for row in [int(img_height * j + margins[0]) for j in range(grid[1])]:
            new_button = pygame.Surface((img_width, img_height))
            new_button.blit(sheet, (0, 0), area=[column, row, img_width, img_height])
            new_button = pygame.transform.scale(new_button, (250, 150))
            new_button.set_colorkey(new_button.get_at((0, 0)))
            cut_buttons.append(new_button)
    return cut_buttons


def load_all(path: str, imgs_dict: dict = {}) -> dict:
    """Recursive method that loads all the images in a directory and its subdirectories
    key = image file name without extension, value = pygame.Surface

    Args:
        path (str): Head directory
        imgs_dict (dict): dictionary to add images to. Creates new one if None is passed.

        Returns:
            Dictionary where { key = image file name excluding extension, value = pygame.Surface }
    """
    _cpath = None
    for _file in os.listdir(path):
        _cpath = os.path.join(path, _file)
        if os.path.isdir(_cpath):
            load_all(os.path.abspath(os.path.join(path, _file)), imgs_dict)

        elif os.path.isfile(_cpath):
            imgs_dict[_file.split(".")[0]] = pygame.image.load(
                os.path.join(path, _file)
            )

    return imgs_dict
