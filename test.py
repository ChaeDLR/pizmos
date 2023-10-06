import pizmos
import test


if __name__ == "__main__":
    # region image tests

    test.image.load_all(pizmos.image.load_all)

    # endregion

    # region pixel tests

    test.pixel.get_surfcolors(pizmos.pixel.get_surfcolors)
    test.pixel.replace_color(pizmos.pixel.replace_color)
    test.pixel.coloredsurf(pizmos.pixel.coloredsurf)

    # endregion
