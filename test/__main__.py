import sys

try:
    import pizmos
    import pygame

    print(
        f"{pizmos.__title__} {pizmos.__version__} (python {sys.version.split(' ')[0]})"
    )
except ModuleNotFoundError:
    raise
