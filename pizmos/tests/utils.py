import pygame

from secrets import randbelow

def coloredsurf(size: tuple=(64, 64)) -> pygame.Surface:
    _surf = pygame.Surface(
            size,
            flags=pygame.BLEND_ALPHA_SDL2 | pygame.SRCALPHA
        )
    _colors = [
            (randbelow(256), randbelow(256), randbelow(256), (255)) for _ in range(4)
        ]

    _cw, _ch = size[0]//2, size[1]//2
    for i in range(2):
        _surf.fill(_colors.pop(),(_cw*i, 0, _cw, _ch))
        _surf.fill(_colors.pop(), (_cw*i, _ch, _cw, _ch))
    return _surf
