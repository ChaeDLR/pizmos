from random import randint
from pygame import Vector2

if __name__ == "__main__":
    from particle import Particle
else:
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
        flags=pygame.SRCALPHA,
        display=0,
        vsync=1,
    )
    window_rect: pygame.Rect = window.get_rect()

    clock: pygame.time.Clock = pygame.time.Clock()

    pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN])

    updates: list[pygame.Rect] = []

    pygame.font.init()
    font_size = 16
    _font = pygame.font.SysFont(None, font_size)

    _text_column = display_info.current_w // 16
    _text_row = display_info.current_h // 12
    text_positions: list[Vector2] = [
        Vector2(_text_column, _text_row * (i + 1)) for i in range(len(_effects))
    ]

    assert text_positions[-1].y < (display_info.current_h - font_size)

    effects_text = {"selected": [], "nonselected": []}
    for i, name in enumerate(_effects.keys()):
        effects_text["selected"].append(
            (_font.render(name, True, (255, 255, 255, 255), (0, 0, 0, 255)), text_positions[i])
        )

        effects_text["nonselected"].append(
            (_font.render(name, True, (0, 0, 0, 255), (255, 255, 255, 255)), text_positions[i])
        )

    while 1:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        window.fill((255, 255, 255, 255))

        updates.append(window.blits(effects_text["nonselected"]))

        #pygame.display.update(updates[:]) # does not work with opengl
        pygame.display.flip()
        updates.clear()
