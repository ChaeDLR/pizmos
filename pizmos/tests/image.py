import pygame
import pizmos

from sys import exit, exc_info
from typing import Callable, Iterable
from secrets import randbelow


def __launch_window() -> None:
    pygame.display.init()
    idisplay = pygame.display.Info()

    display: pygame.Surface = pygame.display.set_mode(
        size=(idisplay.current_w//2, idisplay.current_h//2),
        flags=pygame.SCALED,
        display=0,
        vsync=1,
    )

    clock = pygame.time.Clock()

    pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN])

    live_particles: list = []
    while 1:
        clock.tick(60)
        display.fill((10, 10, 10, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    live_particles.extend(
                        pizmos.particles.explosion(start_position=event.pos)
                    )

        ####### update and draw #######
        if 0 < len(live_particles):
            for particle in live_particles:
                particle.update()

                if particle.alpha == 0:
                    live_particles.remove(particle)
                else:
                    pygame.draw.circle(
                        surface=display,
                        color=particle.color,
                        center=particle.center,
                        radius=particle.radius,
                    )
        pygame.display.update()


def from_image_file(
            func: Callable[[Iterable, str], pygame.Surface],
            _case=[]
        ) -> tuple[int, int]:
    """
    (rectangle, filepath) -> Surface
    """
    pass

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
        for i in range(4):
            for j in range(4):
                testSurf.fill(
                        color=(randbelow(256), randbelow(256), randbelow(256), 255),
                        rect=(_x*i, _y*j, _w, _h)
                    )

        func(testSurf)
    except TypeError as ex:
       print("\nInvalid argument passed to test method.\n")
       raise ex.with_traceback(exc_info()[2].tb_next)

def get_subimages(
            func: Callable[[pygame.Surface, Iterable],
            list[pygame.Surface]],
            _case=[]
        ) -> tuple[int, int]:
    """
    (Surface, size) -> list[Surface]
    """
    pass

def trim(
            func: Callable[[pygame.Surface],
            tuple[pygame.Surface, pygame.Rect]],
            _case=[]
        ) -> tuple[int, int]:
    """
    (Surface) -> tuple[Surface, Rect]
    """
    print("trim")
    pass

def slicendice(
                func: Callable[[pygame.Surface, Iterable, Iterable],
                list[pygame.Surface]],
                _case=[]
            ) -> tuple[int, int]:
    """
    (Surface, grid: tuple[int, int], margins: tuple) -> list[Surface]
    """
    pass
