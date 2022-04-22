import pygame
import os

from sys import exc_info


def load(path: str) -> dict:
        """
        Recursive function that returns a directory
        with all the images in the path arg directory
        """
        def __load(imgs_dict: dict, prev_key: str=None) -> dict:
            if prev_key:
                imgs_dict[prev_key] = {}
            _size: tuple = (64, 64)
            _imgs: list = []

            try:
                img: pygame.Surface = None
                str_parts: list[str] = None
                for file in os.listdir(path):
                    if file[len(file) - 4 :] == ".png":
                        img = pygame.transform.scale(
                            pygame.image.load(os.path.join(path, file)).convert_alpha(),
                            _size,
                        )
                        img.set_colorkey(img.get_at((0,0)))

                        if file[:-4].isdigit():
                            _imgs.append(img)
                        else:
                            # single .pngs with their key in the title
                            str_parts = file[:-4].split("_")
                            imgs_dict[str_parts[0]] = img

                    else:
                        if prev_key:
                            load(
                                os.path.abspath(os.path.join(path, file)),
                                imgs_dict[prev_key],
                                file,
                            )
                        else:
                            load(
                                os.path.abspath(os.path.join(path, file)),
                                imgs_dict,
                                file,
                            )
            except NotADirectoryError as ex:
                print(f"{ex.filename} not an accepted file type.")
                raise ex.with_traceback(exc_info())

            if len(_imgs) > 0:
                imgs_dict[prev_key] = _imgs

            return imgs_dict
        return __load({})

def from_image_file(
        rectangle: tuple[int, int, int, int],
        filepath: str,
    ) -> pygame.Surface:
        """Load a rectangle"""
        # Loads image from x, y, x+offset, y+offset
        image = pygame.Surface(rectangle[:2]).convert()
        image.blit(pygame.image.load(filepath), (0, 0), rectangle)
        return image

def get_surfcolors(img: pygame.Surface) -> tuple:
        """
        Loop through a surface and grab the colors its made of
        sort from lightest(n) to darkest(0)
        """
        excluded = [
            [255, 255, 255, 255],
            [0, 0, 0, 255],
        ]
        if _cc := img.get_colorkey(): excluded.append(list(_cc))

        colors = list()
        pixel_color = list()
        for row in pygame.surfarray.array3d(img):
            for pixel in row:
                pixel_color = [int(pixel[0]), int(pixel[1]), int(pixel[2]), 255]
                if pixel_color not in excluded + colors:
                    colors.append(pixel_color)
        colors.sort(key=sum)
        return tuple(colors)

def get_subimages(image: pygame.Surface, size: tuple=None) -> list[pygame.Surface]:
    """
    return a list of surfaces from the given surface
    divided by the color at (0,0)
    """
    _img = image
    _colorkey = _img.get_at((0, 0))
    _mask = pygame.mask.from_surface(_img, threshold=174)
    _rects = _mask.get_bounding_rects()

    _images = list()
    for (surf, rect) in [
        (
            pygame.Surface(
                _rect.size,
                flags=pygame.BLEND_ALPHA_SDL2,
            ),
            _rect,
        )
        for _rect in _rects
    ]:
        surf.blit(_img, (0, 0), area=rect)
        surf.set_colorkey(_colorkey)
        _images.append(surf)

    try:
        return list(
            map(
                pygame.transform.scale,
                [_img for _img in _images],
                [size for _ in range(len(_images))],
            )
        )
    except:
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
    # TODO: make square with random rect algorithm
    surf = pygame.Surface(size, flags=pygame.BLEND_ALPHA_SDL2 | pygame.SRCALPHA)


class Image:
    name: str = ""
    next: "Image" = None

    __image: pygame.Surface = None
    __rect: pygame.Rect = None

    def __init__(
        self, surface: pygame.Surface, pos: tuple[int, int] = (0, 0), **kwargs
    ) -> None:
        self.image = surface
        self.rect = self.image.get_rect(center=pos)

        for key in kwargs:
            try:
                self.__setattr__(key, kwargs[key])
            except ValueError:
                print(f"Failed to set attr {key}: {kwargs[key]}")

    @property
    def image(self) -> pygame.Surface:
        return self.__image

    @image.setter
    def image(self, value: pygame.Surface) -> None:
        if isinstance(value, pygame.Surface):
            self.__image = value
            if self.__rect:
                self.__rect = value.get_rect(center=self.__rect.center)
        else:
            raise ValueError(f"{value} must be an instance of pygame.Surface.")

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect

    @rect.setter
    def rect(self, value: pygame.Rect) -> None:
        if isinstance(value, pygame.Rect):
            self.__rect = value
        else:
            raise ValueError(f"{value} must be an instance of pygame.Rect.")

    def resize(self, w_h: tuple[int, int]) -> None:
        self.image = pygame.transform.scale(self.image, w_h)
        self.rect = self.image.get_rect()

    def set_position(self, x_y: tuple[int, int]) -> None:
        """set using rect center"""
        self.rect.center = x_y
