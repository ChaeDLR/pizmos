from pygame import Vector2, Surface, draw


class Particle:

    color: list[int, int, int, int]
    center: Vector2
    slope: tuple[int, int]
    radius: float

    def __init__(
        self, color: list, center: Vector2 | tuple, slope: tuple | list, radius: float
    ) -> None:
        self.color = color
        self.center = center
        self.slope = slope
        self.radius = radius

        # the larger the particle the lower the dissipation rate
        self.__dissipation_rate: float = 6 / self.radius

    # region properties

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

    @property
    def dissipation_rate(self) -> float:
        return self.__dissipation_rate

    @dissipation_rate.setter
    def dissipation_rate(self, value: float | int) -> None:
        if value > 0:
            self.__dissipation_rate = value

    # endregion

    def update(self, **kwargs) -> None:
        """Update particle position and alpha values"""
        self.center.x += self.slope[0]
        self.center.y += self.slope[1]

        self.alpha -= self.__dissipation_rate


class Group:

    __update_rects = []
    __index = 0
    __particles = None

    def __init__(self, particles: list[Particle] = []):
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

    def add(self, particle: Particle) -> None:
        if isinstance(particle, Particle):
            self.__particles.append(Particle)
        else:
            raise ValueError(f"{particle} is not an instance of Particle.")

    def update(self, **kwargs) -> None:
        for _particle in self.__particles:
            _particle.update(kwargs)
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
