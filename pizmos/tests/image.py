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