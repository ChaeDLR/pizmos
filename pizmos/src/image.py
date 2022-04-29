import pygame

from secrets import randbelow


def get_subimage(
        rectangle: tuple[int, int, int, int],
        filepath: str,
    ) -> pygame.Surface:
        """
        returns a subimage of the given rect 
        """
        image = pygame.Surface(
            rectangle[:2], 
            flags=pygame.BLEND_ALPHA_SDL2 | pygame.SRCALPHA
        )
        image.blit(pygame.image.load(filepath), (0, 0), rectangle)
        return image

def get_subimages(image: pygame.Surface) -> list[pygame.Surface]:
    """
    return a list of surfaces from the given surface
    divided by the color at (0,0)
    """
    _img = image
    _colorkey = _img.get_at((0, 0))
    _mask = pygame.mask.from_surface(_img, threshold=174)
    _images = list()

    for (surf, rect) in [
        (
            pygame.Surface(
                _rect.size,
                flags=pygame.BLEND_ALPHA_SDL2 | pygame.SRCALPHA,
            ),
            _rect,
        ) for _rect in _mask.get_bounding_rects()
    ]:
        surf.blit(_img, (0, 0), area=rect)
        surf.set_colorkey(_colorkey)
        _images.append(surf)
    return _images

def trim(image: pygame.Surface) -> tuple[pygame.Surface, pygame.rect.Rect]:
    """
    Remove as much of the colorkey as possible
    """
    _img = image
    _mask: pygame.mask.Mask = pygame.mask.from_surface(_img)
    _rect: pygame.rect.Rect = _mask.get_bounding_rects()[0]
    image = pygame.Surface(_rect.size, flags=pygame.BLEND_ALPHA_SDL2)
    image.blit(_img, (0, 0), area=_rect)
    image.set_colorkey(image.get_at((0, 0)))
    return (image, pygame.rect)


def slicendice(
        sheet: pygame.Surface, grid: tuple[int, int], margins: tuple = (0, 0, 0, 0)
    ) -> list[pygame.Surface]:
    """
    cut the spritesheet by the given dimensions
    grid: tuple[col, rows]
    margins: tuple[top, bottom, left, right]
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

def generate_surface(size: tuple[int, int]) -> pygame.Surface:
    """
    Generate a surface with random rects filled with random colors
    """
    surf = pygame.Surface(size, flags=pygame.BLEND_ALPHA_SDL2 | pygame.SRCALPHA)
    initial_rect: tuple = (0, 0, randbelow(size[0]), randbelow(size[1]))

    wside = list()
    hside = list()
    c_w, c_h = initial_rect[2], initial_rect[3]

    while c_w != size[0]:
        offset_w = size[0] - c_w
        offset_h = size[1] - c_h
        n_w = randbelow(offset_w)
        wside.append(
            (c_w, c_h, n_w, randbelow(offset_h))
        )
        c_w += n_w
    print(wside)

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
