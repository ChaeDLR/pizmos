from pygame import Vector2, Surface, draw, Rect

from traceback import print_stack
from sys import stderr

"""
A = np.ones((2, 2))
B = np.eye(2, 2)
C = np.zeros((2, 2))
D = np.diag((-3, -4))
np.block([[A, B], [C, D]])
array([[ 1.,  1.,  1.,  0.],
       [ 1.,  1.,  0.,  1.],
       [ 0.,  0., -3.,  0.],
       [ 0.,  0.,  0., -4.]])
"""


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
        dissipation_rate: float = None,
    ) -> None:
        self.color = list(color)
        if len(self.color) < 4:
            self.color.append(255)
        self.center = list(center)
        self.slope = slope
        self.radius = radius

        # the larger the particle the lower the dissipation rate
        if dissipation_rate:
            self.__dissipation_rate: float = 255 * dissipation_rate
        else:
            self.__dissipation_rate = 6 / self.radius

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

    def update(self, **kwargs: dict) -> None:
        """Update particle position and alpha values
        until self.expired returns true
        """
        self.center[0] += self.slope[0]
        self.center[1] += self.slope[1]
        self.alpha -= self.__dissipation_rate


class Group:
    """Contain and manage groups of particles

    Raises:
        StopIteration: __next__
        ValueError: self.add(), only accept Particle type

    Example:
        effect: ParticleGroup = pizmos.effects.blip(**kwargs)
        effect.update()
        update_rects = effect.draw(window)
        pygme.display.update(update_rects)
    """

    __index = 0
    # start with 10 rows with 10 cols each until more space is needed
    __particles: list = []

    def __init__(self, particles: list[Particle] = []):
        self.__particles = list(particles)

    def __len__(self) -> int:
        return len(self.__particles)

    def __bool__(self) -> bool:
        return bool(self.__particles)

    def __iter__(self):
        # TODO: this might return the wrong value
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
        and remove expired.
        """
        for _particle in self.__particles:
            _particle.update(**kwargs)
            if _particle.expired:
                self.__particles.remove(_particle)
                del _particle

    def draw(self, window: Surface) -> list[Rect]:
        """Draw all particles to given surface

        Args:
            window (Surface): target canvas

        Returns:
            iterable of rects that need to be updated
            by pygame.display.update(rects)
        """
        try:
            return [
                draw.circle(
                    surface=window,
                    color=_particle.color,
                    center=_particle.center,
                    radius=_particle.radius,
                )
                for _particle in self.__particles
            ]
        except ValueError as ex:
            print_stack(file=stderr)
            raise ex
