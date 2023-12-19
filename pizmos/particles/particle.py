from pygame import Vector2, Surface, draw
from numpy import ndarray, array


class Particle:
    """Particle class
    color: rgba,
    center: (x, y),
    slope: (0, 0),
    radius: float, r >= 1

    Usage:
        while 1:
            particle.update()
            draw(particle)
    """

    color: list[int, int, int, int] = []
    center: Vector2 = Vector2()
    slope: tuple[int, int] = (0, 0)
    radius: float = 1.0

    def __init__(
        self,
        color: list,
        center: Vector2 | list | tuple,
        slope: tuple | list,
        radius: float,
        dissipation_rate:float=None
    ) -> None:
        self.color = [0,0,0,255]
        for i, _c in enumerate(color):
            self.color[i] = _c
        self.center = list(center)
        self.slope = slope
        self.radius = radius

        # the larger the particle the lower the dissipation rate
        self.__dissipation_rate: float = dissipation_rate if dissipation_rate else 20 / self.radius

    # region properties

    @property
    def expired(self) -> bool:
        if self.alpha == 0 or self.radius < 1:
            return True
        return False

    @property
    def alpha(self) -> int:
        return self.color[3]

    @alpha.setter
    def alpha(self, value: float) -> None:
        if value < 10:
            self.color[3] = 0
        elif value > 255:
            self.color[3] = 255
        else:
            self.color[3] = value

    @property
    def dissipation_rate(self) -> float:
        return self.__dissipation_rate

    @dissipation_rate.setter
    def dissipation_rate(self, value: float | int) -> None:
        if value > 0:
            self.__dissipation_rate = value

    # endregion

    def update(self, kwargs: dict) -> None:
        """Update particle position and alpha values
        until self.expired returns true
        """
        self.center[0] += self.slope[0]
        self.center[1] += self.slope[1]

        self.alpha -= self.__dissipation_rate


class ParticleGroup:
    """Contain and manage groups of particles

    Raises:
        StopIteration: __next__
        ValueError: self.add(), only accept Particle type

    """

    __update_rects = []
    __index = 0
    __particles: list = []
    __size: int = 10

    def __init__(self, particles: list[Particle] = []):
        self.__particles = list(particles)

    def __len__(self) -> int:
        """
        Returns:
            int: nparray.size
        """
        return self.__particles.size

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

    def add(self, particle: Particle) -> None:
        if isinstance(particle, Particle):
            self.__particles.append(Particle)
        else:
            raise ValueError(f"{particle} is not an instance of Particle.")

    def update(self, **kwargs) -> None:
        """Call all particle update methods
        and remove expired
        """
        for _particle in self.__particles:
            _particle.update(kwargs)
            if _particle.expired:
                self.__particles.remove(_particle)
                del _particle

    def draw(self, window: Surface) -> None:
        """Draw all particles to given surface

        Args:
            window (Surface): target canvas

        Returns:
            None
        """
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
