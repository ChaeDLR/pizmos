import pygame

from collections.abc import Sequence


def get_subimages(sheet: pygame.Surface) -> list[pygame.Surface]:
    """get subimages from a given surface

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

    for (surf, rect) in [
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
    sheet: pygame.Surface, grid: Sequence[int, int], margins: tuple = (0, 0, 0, 0)
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
        for row in [int(img_height * i + margins[0]) for i in range(grid[1])]:
            new_button = pygame.Surface((img_width, img_height))
            new_button.blit(sheet, (0, 0), area=[column, row, img_width, img_height])
            new_button = pygame.transform.scale(new_button, (250, 150))
            new_button.set_colorkey(new_button.get_at((0, 0)))
            cut_buttons.append(new_button)
    return cut_buttons
