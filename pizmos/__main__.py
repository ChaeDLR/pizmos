import sys
print(sys.argv)

try:
    if sys.argv[1] == "test":
        from .tests import run
        run()
except (IndexError, ModuleNotFoundError) as ex:
    raise ex.with_traceback(sys.exc_info())