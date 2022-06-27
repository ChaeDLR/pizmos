from random import randint
from pygame import Vector2
from .particle import Particle


def explosion(start_position: Vector2) -> list[Particle]:
    """Creates Particle list with explosion slopes

    Args:
        start_position (Vector2): x and y values

    Returns:
        list[Particle]: All the Particles that make up the effect
    """
    particles: list[Particle] = []

    # modifiers for a particles (x, y) movement
    # (-1) -> invert
    # 0 -> zero out increment. Do not move across the axis
    # 1 -> keep the default direction
    directions: tuple[tuple[int, int]] = (
        # left   # right # up     # down  # topleft
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
        (-1, -1),
        # botleft# tpright#botright
        (-1, 1),
        (1, -1),
        (1, 1),
    )

    colors = [
        [randint(20, 230), randint(20, 230), randint(20, 230), 255] for _ in range(4)
    ]

    velocity: int = 20

    # this loop creates a new particle layer
    # color, radius, rate of change
    for i, color in enumerate(colors, 1):  # layer

        # get the percentage this particle's ROC should be
        # 100% = full speed
        # higher velocity and lower radius = faster particle movement and alpha ROC
        roc_percentage: float = (velocity / i) / velocity  # try asking Hope

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


if __name__ == "__main__":
    import pygame

    _effects = {"explosion": explosion}

    pygame.display.init()
    display_info = pygame.display.Info()

    window: pygame.Surface = pygame.display.set_mode(
        size=(display_info.current_w // 2, display_info.current_h // 2),
        flags=pygame.SCALED | pygame.BLEND_ALPHA_SDL2,
        display=0,
        vsync=1,
    )
    window_rect: pygame.Rect = window.fill((10, 10, 10, 255))

    clock: pygame.time.Clock = pygame.time.Clock()

    pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN])

    updates: list[pygame.Rect] = []

    _font = pygame.font.Font(size=16)
    effects_text = []
    for name in _effects.keys():
        effects_text.append(_font.render(name, True, (255, 255, 255), (10, 10, 10)))

    while 1:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        # tuple[Surface, coord]
        # window.blits()

        pygame.display.update(updates[:])
        updates.clear()
