from dataclasses import dataclass
from pygame import Vector2, Surface, draw


@dataclass
class Particle:

    color: list[int, int, int, int]
    center: Vector2
    slope: tuple[int, int]
    radius: float

    def __post_init__(self):
        self.__dissipation_rate: float = 6 / self.radius

    @property
    def alpha(self) -> int:
        return self.color[3]

    @alpha.setter
    def alpha(self, value: float) -> None:
        if value < 20:
            self.color[3] = 0
        elif value > 255:
            self.color[3] = 255
        else:
            self.color[3] = value

    def update(self) -> None:
        """update the particles values"""
        self.center.x += self.slope[0]
        self.center.y += self.slope[1]

        self.alpha -= self.__dissipation_rate


class Group:

    __particles = []
    __update_rects = []
    __index = 0

    def __init__(self, particles: list[Particle]):
        self.__particles = particles

    def __len__(self) -> int:
        return len(self.__particles)

    def __bool__(self) -> bool:
        return bool(self.__particles)

    def __iter__(self):
        return self

    def __next__(self) -> Particle:
        try:
            self.__index += 1
            return self.__particles[self.__index - 1]
        except IndexError:
            self.__index = 0
            raise StopIteration

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({len(self.__particles)} particles)>"

    def update(self) -> None:
        for _particle in self.__particles:
            _particle.update()
            if _particle.alpha == 0:
                self.__particles.remove(_particle)
                del _particle

    def draw(self, window: Surface) -> None:

        self.__update_rects.clear()

        for _particle in self.__particles:
            self.__update_rects.append(
                draw.circle(
                    surface=window,
                    color=_particle.color,
                    center=_particle.center,
                    radius=_particle.radius,
                )
            )
        return self.__update_rects
