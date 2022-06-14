import pygame
import os
import json

from collections.abc import Sequence
from typing import Callable


def replace_color(func: Callable[[pygame.Surface], Sequence]):
    """
    replace_color(surf: pygame.Surface, old: Sequence, new: Sequence)
    """
    if not callable(func):
        raise TypeError

    testsurf = pygame.Surface((64, 64))
    testsurf.fill((200, 200, 200, 255))

    old = list(testsurf.get_at((1, 1)))
    new = [  # check if pixels3d returns an RGBA format
        255 - old[0],
        255 - old[1],
        255 - old[2],
    ]
    altered_surf = func(testsurf, old, new)
    altered_new = altered_surf.get_at((1, 1))
    new.append(255)
    assert list(altered_new) == new


def get_surfcolors(func: Callable[[pygame.Surface], tuple]):
    """
    (Surface) -> Sequence
    """
    if not callable(func):
        raise TypeError

    _colors = list()
    with open(os.path.abspath("./test/cases/surfcolors.json"), "r") as sctext:
        _loaded: dict = json.load(sctext)

    for i in _loaded.popitem()[1]:
        _colors.append(i)
    testsurf = pygame.Surface((64, 64))
    testrect = testsurf.get_rect()

    _cw, _ch = testrect.w // 2, testrect.h // 2
    # fill surface with colors loaded from json
    for i in range(2):
        testsurf.fill(_colors.pop(), (_cw * i, 0, _cw, _ch))
        testsurf.fill(_colors.pop(), (_cw * i, _ch, _cw, _ch))

    readcolors = [
        list(testsurf.get_at(_xy))
        for _xy in [
            testrect.topleft,
            (testrect.width - 1, 0),
            (0, testrect.height - 1),
            (testrect.width - 1, testrect.height - 1),
        ]
    ]

    for _color in func(testsurf):
        assert _color in readcolors


def coloredsurf(func: Callable[[Sequence], pygame.Surface]):
    if not isinstance(func, Callable):
        raise TypeError
    test_surf = func((120, 120))
    assert isinstance(test_surf, pygame.Surface)
