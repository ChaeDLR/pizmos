from dataclasses import dataclass
from pygame import Vector2


@dataclass
class Particle:

    color: list[int, int, int, int]
    center: Vector2
    slope: tuple[int, int]
    radius: float

    def __post_init__(self):
        self.__dissipation_rate: float = 5 / self.radius

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
    __index = 0

    def __init__(self, particles: list[Particle]):
        self.__particles = particles

    def __iter__(self):
        return self

    def __next__(self) -> Particle:
        try:
            self.__index += 1
            return self.__particles[self.__index - 1]
        except IndexError:
            self.__index = 0
            raise StopIteration

    def update(self) -> None:
        for _particle in self.__particles:
            _particle.update()
