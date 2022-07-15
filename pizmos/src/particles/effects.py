from random import randint
from pygame import Vector2

if __name__ == "__main__":
    from particle import Particle, Group as ParticleGroup
else:
    from .particle import Particle, group as ParticleGroup


def explosion(start_position: Vector2) -> ParticleGroup:
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

    return ParticleGroup(particles)


if __name__ == "__main__":
    import pygame

    class _Effect:
        name: str = None
        selected: bool = False

        select_text: pygame.Surface = None
        nonselect_text: pygame.Surface = None
        text_rect: pygame.Rect = None

        get_particles: callable = None

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
            self.name = self.get_particles.__name__

    #### Add new effects for testing here ####
    _effects: list[_Effect] = [_Effect(get_particles=explosion)]

    # region set display
    pygame.display.init()
    pygame.font.init()

    display_info = pygame.display.Info()

    window: pygame.Surface = pygame.display.set_mode(
        size=(display_info.current_w // 2, display_info.current_h // 2),
        flags=pygame.SRCALPHA,
        display=0,
        vsync=1,
    )

    window_rect: pygame.Rect = window.get_rect()

    clock: pygame.time.Clock = pygame.time.Clock()

    pygame.event.set_allowed(
        [pygame.QUIT, pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]
    )
    # endregion

    # region create text
    font_size = 20
    _font = pygame.font.SysFont(None, font_size)

    _text_column = display_info.current_w // 28
    _text_row = display_info.current_h // 24
    text_positions: list[Vector2] = [
        Vector2(_text_column, _text_row * (i + 1)) for i in range(len(_effects))
    ]

    assert text_positions[-1].y < (
        display_info.current_h - font_size
    ), "Unsupported display size."

    for i, _effect in enumerate(_effects):
        _effect.select_text = _font.render(
            _effect.get_particles.__name__, True, (255, 255, 255, 255), (0, 0, 0, 255)
        )

        _effect.nonselect_text = _font.render(
            _effect.get_particles.__name__, True, (0, 0, 0, 255), (255, 255, 255, 255)
        )

        _effect.text_rect = _effect.select_text.get_rect(topleft=text_positions[i])

    # texts that should be displayed in the window paired with their rect
    active_texts = [[_effect.nonselect_text, _effect.text_rect] for _effect in _effects]

    # active effect index
    active_index = 0

    # set the first effect as active
    active_texts[active_index][0] = _effects[active_index].select_text

    # endregion

    # stores rects of areas that should be updates in the window
    updates: list[pygame.Rect] = []

    # stores live particles
    particles: list[ParticleGroup] = []

    while 1:
        clock.tick(60)

        # region events/update

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            elif event.type == pygame.MOUSEMOTION:
                for _effect in _effects:
                    if _effect.text_rect.collidepoint(event.pos):

                        # set the previous active effect to nonselect
                        active_texts[active_index][0] = _effects[
                            active_index
                        ].nonselect_text

                        # get new active index
                        active_index = _effects.index(_effect)

                        # set new active text
                        active_texts[active_index][0] = _effects[
                            active_index
                        ].select_text

            elif event.type == pygame.MOUSEBUTTONDOWN:
                particles.append(_effects[active_index].get_particles(event.pos))

        # endregion

        # region draw

        window.fill((255, 255, 255, 255))

        for particle in particles:
            particle.update()
            particle.draw(window)
            # TODO: remove empty particle groups

        updates.append(window.blits(active_texts))

        # endregion

        # pygame.display.update(updates[:]) # TODO: does not work with opengl, need to add check
        pygame.display.flip()
        updates.clear()
