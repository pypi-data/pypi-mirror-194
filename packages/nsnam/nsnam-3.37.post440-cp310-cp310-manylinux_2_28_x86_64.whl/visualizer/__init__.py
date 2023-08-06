# This is a stub module that loads the actual visualizer
# from nsnam.visualizer
import sys

try:
    import nsnam.visualizer
except ModuleNotFoundError as e:
    print("Install the nsnam package with pip install nsnam.", file=sys.stderr)
    exit(-1)

from nsnam.visualizer import start, register_plugin, set_bounds, add_initialization_hook
