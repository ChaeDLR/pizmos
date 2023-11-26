"""Components that update every cycle
"""

from traceback import print_stack
from pygame import Surface, SRCALPHA, Rect, font


class ProgressBar:
    """Dynamic
    Bar ui element
    """

    image: Surface = None
    rect: Rect = None
    base_color: tuple = None
    color: tuple = None
    size: tuple = None

    __percentage: float = 1.0
    __get_percentage_cb: callable = None

    def __init__(
        self,
        position: tuple | list,
        size: tuple | list,
        color: tuple | list,
        percentage_cb: callable,
    ) -> None:
        """Progress bar component meant to be displayed on pygame Surfaces

        Args:
            size (tuple | list): total size
            color (tuple | list): _description_
            percentage_cb (callable): _description_
        """
        self.set_percentage_cb(percentage_cb)
        self.size = size
        self.image = Surface(size, flags=SRCALPHA)
        self.image.fill((10, 10, 10, 200))

        self.color = color
        self.base_color: tuple = (10, 10, 10, 200)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position[0], position[1]

    def set_percentage_cb(self, percentage_cb: callable) -> None:
        """Set the call back function that returns a value from [0.0, 1.0]
        that represents the peercentage of the bar that should be displayed

        Args:
            percentage_cb (callable): callable function that returns a float value in range(0.0, 1.0)

        Raises:
            Exception: Invalid argument
            Exception: Invalid return type from callable argument

        Returns:
            None
        """
        if not callable(percentage_cb):
            print_stack()
            raise Exception(f"Invalid argument: {percentage_cb}\nExpected callable.")
        self.__get_percentage_cb = percentage_cb
        try:
            self.__percentage = float(self.__get_percentage_cb())
        except:
            print_stack()
            raise Exception(
                f"Invalid callable: {percentage_cb}\nExpected return value of type float."
            )

    def update(self) -> None:
        """Take the players current health percentage
        to the nearest whole number
        """
        self.__percentage = self.__get_percentage_cb()
        _img = Surface(
            ((self.size[0] * self.__percentage) - 20, self.rect.height - 10)
        ).convert()
        _img.fill(self.color)

        self.image.fill(self.base_color)
        self.image.blit(
            _img,
            (
                self.rect.x,
                self.rect.y - 5,
            ),
        )


class TextSurface:
    """Dynamic
    Text Surface

    Raises:
        Exception: _description_
        Exception: _description_
        Exception: _description_

    Returns:
        _type_: _description_
    """

    image: Surface = None
    rect: Rect = None

    __text: str = ""
    __text_color: tuple = (120, 174, 90, 255)
    __text_font: font.Font = None
    __text_update_cb: callable = None

    def __init__(
        self, position: tuple | list, font_size: int, text_update_cb: callable
    ) -> None:
        self.__text_font = font.SysFont(None, font_size, bold=True)
        self.image, self.rect = self.__create_text((10, 10))
        self.rect.x, self.rect.y = position[0], position[1]

        if not callable(text_update_cb):
            print_stack()
            raise Exception(f"Invalid argument: {text_update_cb}\nExpected callable.")
        self.__text_update_cb = text_update_cb
        try:
            self.__text = str(self.__text_update_cb())
        except:
            print_stack()
            raise Exception(
                f"Invalid callable: {text_update_cb}\nExpected return value of type string."
            )

    def __create_text(self, x_y: tuple) -> tuple[Surface, Rect]:
        """
        x_y: tuple -> positions using center of the rect
        Tuple -> (text_img, text_rect)
        """
        text_img = self.__text_font.render(self.__text, 1, self.__text_color)
        text_rect = text_img.get_rect()
        text_rect.center = x_y
        return (text_img, text_rect)

    def set_text(self, txt: str) -> None:
        """Set the components text

        Args:
            txt (str): Text to be displayed on the image surface.

        Raises:
            Exception: cannot convert to string
        """
        try:
            self.__text = str(txt)
        except TypeError:
            print_stack()
            raise Exception(f"Invalid argument: {txt}\nExpected string.")

    def update(self) -> None:
        self.__text = self.__text_update_cb()
        self.image = self.__text_font.render(self.__text, 1, self.__text_color)
        _pos = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = _pos
