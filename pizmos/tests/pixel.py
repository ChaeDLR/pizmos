import pygame

from sys import exc_info
from secrets import randbelow
from typing import Callable


# TODO
def replace_color(
            func: Callable[[pygame.Surface], tuple],
            _case=[]
        ) -> tuple[int, int]:
    """
    replace_color(surf: pygame.Surface, old: tuple | list, new: tuple | list)
    """
    ...

def get_surfcolors(
            func: Callable[[pygame.Surface], tuple],
            _case=[]
        ) -> tuple[int, int]:
    """
    (Surface) -> tuple
    """
    print("Testing image.get_surfacecolor()...")
    try:
        _x, _y = 480, 320
        _w = _x/4
        _h = _y/4

        testSurf = pygame.Surface(
                (_w, _h),
                flags=pygame.BLEND_ALPHA_SDL2 | pygame.SRCALPHA
            )

        # TODO: map
        # for i in range(4):
        #     for j in range(4):
        #         testSurf.fill(
        #                 color=(randbelow(256), randbelow(256), randbelow(256), 255),
        #                 rect=(_x*i, _y*j, _w, _h)
        #             )

        func(testSurf)
    except TypeError as ex:
       print("\nInvalid argument passed to test method.\n")
       raise ex.with_traceback(exc_info()[2].tb_next)