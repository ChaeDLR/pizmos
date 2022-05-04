import sys

try:
    import pizmos
    import pygame
    import pizmos.tests as tests

    print(f"{pizmos.__title__} {pizmos.__version__} (python {sys.version.split(' ')[0]})")
except ModuleNotFoundError:
    raise

if __name__ == "__main__":

    testsurf = tests.utils.coloredsurf()
    testrect = testsurf.get_rect()
    readcolors = [testsurf.get_at(_xy) for _xy in [
            testrect.topleft, (testrect.width-1, 0),
            (0, testrect.height-1), (testrect.width-1, testrect.height-1)
        ]
    ]

    tests.pixel.get_surfcolors(pizmos.pixel.get_surfcolors)

    pygame.display.init()
    idisplay = pygame.display.Info()

    display: pygame.Surface = pygame.display.set_mode(
            size=(idisplay.current_w//2, idisplay.current_h//2),
            flags=pygame.SCALED,
            display=0,
            vsync=1
        )
    display.fill((230, 215, 212, 255))

    clock = pygame.time.Clock()
    pygame.event.set_allowed(
            [pygame.QUIT, pygame.MOUSEBUTTONDOWN]
        )

    _updates: list = []
    _updates.append(display.blit(testsurf, testsurf.get_rect(
                    center=(
                        display.get_width()//2,
                        display.get_height()//2
                    )
                )
            )
        )
    _CLEARUPDATE = pygame.event.custom_type()
    pygame.time.set_timer(
            pygame.event.Event(_CLEARUPDATE),
            10
        )
    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == _CLEARUPDATE:
                _updates.clear()
        display.blit(testsurf, testsurf.get_rect(
                    center=(
                        display.get_width()//2,
                        display.get_height()//2
                    )
                )
            )

        pygame.display.update(_updates)
