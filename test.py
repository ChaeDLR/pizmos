import pizmos
import test


if __name__ == "__main__":

    # region pixel tests

    test.pixel.get_surfcolors(pizmos.pixel.get_surfcolors)
    test.pixel.replace_color(pizmos.pixel.replace_color)
    test.pixel.coloredsurf(pizmos.pixel.coloredsurf)

    # endregion

    # region image

    test.image.load(pizmos.image.load)

    # endregion
