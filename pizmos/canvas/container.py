from pygame import Rect, Surface


class CanvasContainer:
    rect: Rect = None

    # static and dynamic component containers
    __dynamic_com: list = []
    __static_com: list = []

    def __init__(self, dims: tuple[int, int]) -> None:
        self.rect = Rect(0.0, 0.0, dims[0], dims[1])

    def get_components(self) -> list:
        return [*self.__dynamic_com.copy(), *self.__static_com.copy()]

    def get_blitseq(self) -> list[Surface, Rect]:
        """Get a sequence of tuples

        Returns:
            list[Surface, Rect]: _description_
        """
        return [(i.image, i.rect) for i in self.get_components()]

    def attach(self, *new_components) -> None:
        """Attach a component to the hud to be updated and drawn

        Args:
            component (any): Class should have
            component.rect: pygame.Rect
            component.image: pygame.Surface
            component.update(): method to update component variables
        """
        for component in new_components:
            if not (hasattr(component, "image") and hasattr(component, "rect")):
                raise Exception(
                    f"Component: {component}\nDoes not have attr image and/or rect."
                )
            if hasattr(component, "update"):
                self.__dynamic_com.append(component)
            else:
                self.__static_com.append(component)

    def update(self) -> None:
        for _com in self.__dynamic_comp:
            _com.update()
