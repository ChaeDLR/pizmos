from math import hypot, atan2, sin, cos, pi


def get_directions(start: tuple, stop: tuple) -> tuple:
    """
    Returns the rise and run directions
    from the start to the stop in a tuple
    """
    radians = atan2(stop[1] - start[1], stop[0] - start[0])
    return (cos(radians), sin(radians))


def get_distance(start: tuple, stop: tuple) -> float:
    """
    Returns the distance between two points
    """
    return hypot(stop[0] - start[0], stop[1] - start[1])


def get_angle_to(start: tuple, stop: tuple) -> float:
    """Returns the clockwise angle from start to stop in radians.
    Convert to degrees using math.degrees().

    Args:
        start (tuple): x, y
        stop (tuple): x, y

    Returns:
        float: Angle in degrees
    """
    dx = stop[0] - start[0]
    dy = stop[1] - start[1]
    radians = atan2(-dy, dx)
    radians %= 2 * pi
    return radians
