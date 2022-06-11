import pygame
import os
import json

from typing import Callable


def replace_color(func: Callable[[pygame.Surface], tuple]) -> tuple[int, int]:
    """
    replace_color(surf: pygame.Surface, old: tuple | list, new: tuple | list)
    """
    if not callable(func): raise TypeError

def get_surfcolors(func: Callable[[pygame.Surface], tuple]) -> tuple[int, int]:
    """
    (Surface) -> tuple[int, int]
    """
    if not callable(func): raise TypeError

    _colors = list()
    with open(os.path.abspath("./test/cases/surfcolors.json"), 'r') as sctext:
        _loaded: dict = json.load(sctext)

    for i in _loaded.popitem()[1]:
        _colors.append(i)
    testsurf = pygame.Surface((64, 64))
    testsurf.set_colorkey()
    testrect = testsurf.get_rect()

    _cw, _ch = testrect.w//2, testrect.h//2
    # fill surface with colors loaded from json
    for i in range(2):
        testsurf.fill(_colors.pop(), (_cw*i, 0, _cw, _ch))
        testsurf.fill(_colors.pop(), (_cw*i, _ch, _cw, _ch))

    readcolors = [list(testsurf.get_at(_xy)) for _xy in [
            testrect.topleft, (testrect.width-1, 0),
            (0, testrect.height-1), (testrect.width-1, testrect.height-1)
        ]
    ]

    for _color in func(testsurf):
        assert _color in readcolors
