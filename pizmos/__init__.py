__title__ = "pizmos"
__description__ = "Pizmos: Gizmos for pygame."
__url__ = "https://github.com/ChaeDLR/pizmos"
__version__ = "0.0.1"
__release__ = "0.1"
__author__ = "Chae De La Rosa"
__email__ = "delarosa.chae@gmail.com"
__license__ = "Lesser General Public License"
__copyright__ = "Copyright (C) 2022 Chae De La Rosa"
from os import environ as __environ

__environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from . import image, pixel, math
from . import particles, canvas
from . import parallax_background
