import pygame
import os
import json

from sys import exit
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

    colors = list()
    with open(os.path.abspath("./test/cases/surfcolors.json"), "r") as sctext:
        loaded: dict = json.load(sctext)

    for i in loaded.popitem()[1]:
        colors.append(i)
    testsurf = pygame.Surface((64, 64))
    testrect = testsurf.get_rect()

    cw, ch = testrect.w // 2, testrect.h // 2
    # fill surface with colors loaded from json
    for i in range(2):
        testsurf.fill(colors.pop(), (cw * i, 0, cw, ch))
        testsurf.fill(colors.pop(), (cw * i, ch, cw, ch))

    readcolors = [
        list(testsurf.get_at(_xy))
        for _xy in [
            testrect.topleft,
            (testrect.width - 1, 0),
            (0, testrect.height - 1),
            (testrect.width - 1, testrect.height - 1),
        ]
    ]

    for color in func(testsurf):
        assert color in readcolors


def coloredsurf(func: Callable[[Sequence], pygame.Surface]):
    if not isinstance(func, Callable):
        raise TypeError
    test_surf = func((120, 120))

    assert isinstance(test_surf, pygame.Surface)

    pygame.display.init()
    idisplay = pygame.display.Info()

    display: pygame.Surface = pygame.display.set_mode(
        size=(idisplay.current_w // 2, idisplay.current_h // 2),
        flags=pygame.SCALED,
        display=0,
        vsync=1,
    )
    display.fill((230, 215, 212, 255))

    clock = pygame.time.Clock()
    pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN])

    _updates: list = []
    _updates.append(
        display.blit(
            test_surf,
            test_surf.get_rect(
                center=(display.get_width() // 2, display.get_height() // 2)
            ),
        )
    )
    _CLEARUPDATE = pygame.event.custom_type()
    pygame.time.set_timer(pygame.event.Event(_CLEARUPDATE), 10)
    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == _CLEARUPDATE:
                _updates.clear()
        display.blit(
            test_surf,
            test_surf.get_rect(
                center=(display.get_width() // 2, display.get_height() // 2)
            ),
        )

        pygame.display.update(_updates)
