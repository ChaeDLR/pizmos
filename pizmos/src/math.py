"""
Functions that I use to do 2D math
"""
import math

def get_directions(start: tuple[int, int], stop: tuple[int, int]) -> tuple:
    """
    Returns the rise and run directions
    from the start to the stop in a tuple
    """
    radians = math.atan2(stop[1] - start[1], stop[0] - start[0])
    return (math.cos(radians), math.sin(radians))

def get_distance(start: tuple[int, int], stop: tuple[int, int]) -> float:
    """
    Returns the distance between two points
    """
    return math.hypot(stop[0] - start[0], stop[1] - start[1])

def get_angle_to(start: tuple[int, int], stop: tuple[int, int]) -> float:
    """
    Returns the angle from start to stop in degrees
    """
    radians = math.atan2(
        -(stop[1] - start[1]), stop[0] - start[0]
    )
    radians %= 2 * math.pi
    return math.degrees(radians)
