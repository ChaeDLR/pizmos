from random import randint, choice as rand_choice
from math import pi, cos, sin
from pygame import Vector2

if __name__ == "__main__":
    from particle import Particle, Group as ParticleGroup
else:
    from .particle import Particle, Group as ParticleGroup

# TODO:
# 1. scale effects


def explosion(
    start_position: Vector2 | tuple | list,
    colors: list[list[int, int, int, int]],
    speed: int = 14,
    dissipation_rate: float = 0.18,
) -> ParticleGroup:
    """Creates Particle list with explosion slopes

    Args:
        start_position (Vector2): x and y values

    Returns:
        list[Particle]: All the Particles that make up the effect
    """
    # TODO: particle tails are too long
    particles: list[Particle] = []

    # this loop creates a new particle layer
    # color, radius, rate of change
    for i in range(4, 9):  # layer
        # get the percentage this particle's ROC should be
        # 100% = full speed
        # higher velocity and lower radius = faster particle movement and alpha ROC
        roc_percentage: float = (speed / i) / speed
        for j in range(1, 9):
            _r: float = ((2 * pi) / 9) * j
            _dir = (cos(_r), sin(_r))

            particles.append(
                Particle(
                    rand_choice(colors),
                    center=Vector2(start_position),
                    slope=(
                        (_dir[0] * speed) * roc_percentage,
                        (_dir[1] * speed) * roc_percentage,
                    ),
                    radius=i,
                    dissipation_rate=dissipation_rate,
                )
            )

    return ParticleGroup(particles)


def splat(
    start_position: Vector2 | tuple | list, colors: list[list[int, int, int, int]]
) -> ParticleGroup:
    velocity: int = 20
    pgroup = []
    for i in range(1, 10):
        for j in range(1, 3):
            _r: float = ((2 * pi) / randint(1, 32)) * randint(1, 32)
            _dir = (cos(_r), sin(_r))
            pgroup.append(
                Particle(
                    rand_choice(colors),
                    start_position,
                    (
                        _dir[0] * ((velocity / i)) * j,
                        _dir[1] * ((velocity / i)) * j,
                    ),
                    randint(1, 8),
                )
            )
    return ParticleGroup(pgroup)


def blip(
    start_position: Vector2 | tuple | list, color: list = (100, 100, 100, 250)
) -> ParticleGroup:
    class _Particle(Particle):
        transform_rate: int = 1

        def update(self, kwargs: dict) -> None:
            """transform particle

            Args:
                mouse_pos (Vector2 | tuple, optional): Defaults to (0, 0).
            """
            self.center = kwargs.get("mouse_pos", (1, 1))
            self.radius += self.transform_rate
            if self.radius > 5:
                self.transform_rate -= 1

    return ParticleGroup(
        [_Particle(color, start_position, (0, 0), (i)) for i in range(1, 4)]
    )


#### pygame loop used for testing effects ####
if __name__ == "__main__":
    import pygame

    class _Effect:
        name: str = None
        selected: bool = False

        select_text: pygame.Surface = None
        nonselect_text: pygame.Surface = None
        text_rect: pygame.Rect = None

        get_particles: callable = None
        get_arg: callable = None

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
            self.name = self.get_particles.__name__

    def get_colors() -> list[list[int, int, int, int]]:
        """Get a list of four random colors"""
        return [
            [randint(20, 230), randint(20, 230), randint(20, 230), 255]
            for _ in range(4)
        ]

    def get_color() -> list[int, int, int, int]:
        """Get a single color"""
        return [randint(20, 230), randint(20, 230), randint(20, 230), 255]

    #### Add new effects for testing here ####
    _effects: list[_Effect] = [
        _Effect(get_particles=explosion, get_arg=get_colors),
        _Effect(get_particles=blip, get_arg=get_color),
        _Effect(get_particles=splat, get_arg=get_colors),
    ]

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
            _effect.get_particles.__name__, True, (0, 0, 0, 255), (55, 255, 255, 255)
        )

        _effect.nonselect_text = _font.render(
            _effect.get_particles.__name__, True, (55, 255, 255, 255), (0, 0, 0, 255)
        )

        _effect.text_rect = _effect.select_text.get_rect(topleft=text_positions[i])

    # texts that should be displayed in the window paired with their rect
    active_texts = [[_effect.nonselect_text, _effect.text_rect] for _effect in _effects]

    # active effect index
    active_index = 0

    # set the first effect as active
    active_texts[active_index][0] = _effects[active_index].select_text

    # endregion

    # stores rects of areas that should be updated in the window
    updates: list[pygame.Rect] = []

    # stores live particles
    particles: list[ParticleGroup] = []

    # main test loop
    while 1:
        clock.tick(60)

        # region events/update

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            elif event.type == pygame.MOUSEMOTION:
                for _effect in _effects:
                    # check for effects selection
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
                particles.append(
                    _effects[active_index].get_particles(
                        event.pos, _effects[active_index].get_arg()
                    )
                )

        # endregion

        # region draw

        updates.append(window.fill((5, 5, 5, 255)))

        for particle_group in particles:
            particle_group.update(mouse_pos=pygame.mouse.get_pos())
            updates += particle_group.draw(window)

            # remove empty lists once all the particles have dissipated
            if len(particle_group) == 0:
                particles.remove(particle_group)

        updates += window.blits(active_texts)

        pygame.display.update(updates)
        updates.clear()

        # endregion
