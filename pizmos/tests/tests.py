import sys
from typing import Callable

try:
    from pizmos import (
        image, math, io
    )
except ModuleNotFoundError:
    from .pizmos import (
        image, math, io
    )


def rec_result(test_method: Callable) -> tuple[int, int]:
    """
    This is a decorator for test methods.
    It takes care of
        printing,
        keeping track of fails and passes,
        and returning the results
    """

    def test_callable(cls, callable):

        print(f"\nTesting {callable.__name__} callable.\n")

        passes: int = 0
        fails: int = 0

        for i in range(1, len(cls.cases)):

            print(f"\nTesting case {i}\n{cls.cases[0]}\n{cls.cases[i]}")

            try:
                test_method(cls, callable, _case=cls.cases[i])
                print(f"Test {i} passed.")
                passes += 1
            except:
                print(f"Test {i} failed.")
                fails += 1

        return (passes, fails)

    return test_callable

def exe(test: str, options: list[str]=[]) -> None:
    """Execute all tests unless a test is specified"""
    pass

def run() -> None:
    print("Running!")

if __name__ == "__main__":
    _tests = {
        "generate_surface": image.generate_surface,
        "get_surfcolors": image.get_surfcolors
    }
    # if sys.argv[1] in _tests:
    #     exe(sys.argv[1], )
    # else:
    #     raise f"/nError: {sys.argv[1]} is an invalid test"

    print(sys.argv)
