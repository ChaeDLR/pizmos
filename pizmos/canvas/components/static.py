"""Components that do not update every cycle
"""
from pygame import Surface, Rect, font, transform


class Button:
    """
    Collision: self.rect.collidepoint((x,y))
    Animate: set and reset alpha
    """

    image: Surface = None
    rec: Rect = None

    width: int = 0
    height: int = 0

    text: str = None
    text_font: font.Font = None

    def __init__(
        self,
        image: Surface,
        button_text: str,
        font_size: int,
        name: str = None,
        **kwargs,
    ):
        """Initialize button settings"""
        self.__image_base = image
        self.image = image.copy()
        self.rect = image.get_rect()
        self.text = button_text
        self.font_size = font_size
        self.name = name if name else button_text
        self.set_text(button_text, font_size)

        for key in kwargs:
            try:
                self.__setattr__(key, kwargs[key])
            except ValueError:
                print(f"Failed to set attr {key}: {kwargs[key]}")

    def __str__(self) -> str:
        return self.name

    def resize(self, nrect: Rect | tuple[int, int]) -> None:
        """Resize the button

        Args:
            nrect (Rect | tuple[int,int]): New rect or new (width, height)
        """
        if isinstance(nrect, Rect):
            self.rect = nrect
        else:
            self.rect.width, self.rect.height = nrect

        self.__image_base = transform.scale(self.__image_base, nrect.size)
        self.image = transform.scale(self.image, nrect.size)

    def transparentize(self, intensity: float) -> None:
        """Make button almost completely transparent
        intensity: percentage in range [0.0, 1.0]
        """
        _i: float = 0.0
        if intensity > 1.0:
            _i = 1.0
        elif intensity >= 0.0:
            _i = intensity

        self.set_alpha(_i)
        self.msg_image.set_alpha(_i)

    def reveal(self) -> None:
        """Make button completely visible"""
        self.set_alpha(255)
        self.msg_image.set_alpha(255)

    def clear_text(self) -> None:
        self.msg_image.fill(self.button_color)

    def set_text(self, txt: str, fontsize: int = None) -> None:
        self.text = txt
        if fontsize:
            self.font_size = fontsize
            self.text_font = font.SysFont(None, self.font_size, bold=True)
        self.msg_image = self.text_font.render(self.text, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        self.image = self.__image_base.copy()
        self.image.blit(self.msg_image, self.msg_image_rect)

    def restore_text(self) -> None:
        """
        Display stored text value to the button surface
        """
        self.msg_image = self.text_font.render(self.text, True, self.text_color)
