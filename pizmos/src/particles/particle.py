from dataclasses import dataclass
from random import randint
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
        if value < 20: self.color[3] = 0
        elif value > 255: self.color[3] = 255
        else: self.color[3] = value

    def update(self) -> None:
        """update the particles values"""
        self.center.x += self.slope[0]
        self.center.y += self.slope[1]

        self.alpha -= self.__dissipation_rate
