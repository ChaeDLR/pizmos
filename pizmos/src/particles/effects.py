from random import randint
from pygame import Vector2
from .particle import Particle

def explosion(start_position: tuple[int, int]) -> list[Particle]:
    """
    return a list of particles that have slopes
    that create and explosion effect
    """
    particles: list[Particle] = []

    # modifiers for a particles (x, y) movement
    # (-1) -> invert
    # 0 -> zero out increment. Do not move across the axis
    # 1 -> keep the default direction
    directions: tuple[tuple[int, int]] = (
       # left   # right # up     # down  # topleft
        (-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1),
       # botleft# tpright#botright
        (-1, 1), (1, -1), (1, 1),
    )

    colors = [
        [
            randint(20, 230), randint(20, 230), randint(20, 230), 255
        ] for _ in range(4)
    ]

    velocity: int = 20

    # this loop creates a new particle layer
    # color, radius, rate of change
    for i, color in enumerate(colors, 1):  # layer

        # get the percentage this particle's ROC should be
        # 100% = full speed
        # higher velocity and lower radius = faster particle movement and alpha ROC
        roc_percentage: float = (velocity / i) / velocity # try asking Hope

        for direction in directions:
            particles.append(
                Particle(
                    color=color,
                    center=Vector2(start_position),
                    slope=(
                        (direction[0] * velocity) * roc_percentage,
                        (direction[1] * velocity) * roc_percentage,
                    ),
                    radius=i,
                )
            )

    return particles
