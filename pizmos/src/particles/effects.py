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

    _effects = {
        "explosion": explosion,
        "explosion_spiral": explosion,
        "blip": explosion,
    }

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
    font_size = 20
    _font = pygame.font.SysFont(None, font_size)

    _text_column = display_info.current_w // 28
    _text_row = display_info.current_h // 24
    text_positions: list[Vector2] = [
        Vector2(_text_column, _text_row * (i + 1)) for i in range(len(_effects))
    ]

    assert text_positions[-1].y < (display_info.current_h - font_size)

    effects_text = {"selected": [], "nonselected": [], "rects": []}
    for i, name in enumerate(_effects.keys()):

        text = _font.render(name, True, (255, 255, 255, 255), (0, 0, 0, 255))
        text_rect: pygame.Rect = text.get_rect(topleft=text_positions[i])

        effects_text["selected"].append((text, text_rect))

        effects_text["nonselected"].append(
            (_font.render(name, True, (0, 0, 0, 255), (255, 255, 255, 255)), text_rect)
        )

        effects_text["rects"].append(text_rect)

    active_text = effects_text["nonselected"][:]

    pygame.event.set_allowed(
        [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]
    )

    text_index = 0

    while 1:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect in effects_text["rects"]:
                    if rect.collidepoint(event.pos):
                        active_text[text_index] = effects_text["nonselected"][text_index]
                        text_index = effects_text["rects"].index(rect)
                        active_text[text_index] = effects_text["selected"][text_index]


        window.fill((255, 255, 255, 255))
        updates.append(window.blits(active_text))


        # pygame.display.update(updates[:]) # does not work with opengl
        pygame.display.flip()
        updates.clear()
