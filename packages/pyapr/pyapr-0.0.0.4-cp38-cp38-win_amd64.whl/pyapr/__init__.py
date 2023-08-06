"""Python wrappers for LibAPR

The main package of pyapr contains no features. These are instead available through the following subpackages:

Subpackages
-----------

data_containers
    fundamental data container classes

converter
    templated classes for creating APRs from images of different data types

io
    reading and writing APRs from/to file

numerics
    subpackage for processing using APRs

viewer
    a simple graphical user interface for visualizing results and exploring parameters
"""


""""""  # start delvewheel patch
def _delvewheel_init_patch_0_0_15():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, '.'))
    if sys.version_info[:2] >= (3, 8):
        if os.path.exists(os.path.join(sys.base_prefix, 'conda-meta')):
            # backup the state of the environment variable CONDA_DLL_SEARCH_MODIFICATION_ENABLE
            conda_dll_search_modification_enable = os.environ.get("CONDA_DLL_SEARCH_MODIFICATION_ENABLE")
            os.environ['CONDA_DLL_SEARCH_MODIFICATION_ENABLE']='1'

        os.add_dll_directory(libs_dir)

        if os.path.exists(os.path.join(sys.base_prefix, 'conda-meta')):
            # restore the state of the environment variable CONDA_DLL_SEARCH_MODIFICATION_ENABLE
            if conda_dll_search_modification_enable is None:
                os.environ.pop("CONDA_DLL_SEARCH_MODIFICATION_ENABLE", None)
            else:
                os.environ["CONDA_DLL_SEARCH_MODIFICATION_ENABLE"] = conda_dll_search_modification_enable
    else:
        from ctypes import WinDLL
        with open(os.path.join(libs_dir, '.load-order-pyapr-0.0.0.4')) as file:
            load_order = file.read().split()
        for lib in load_order:
            WinDLL(os.path.join(libs_dir, lib))


_delvewheel_init_patch_0_0_15()
del _delvewheel_init_patch_0_0_15
# end delvewheel patch



from . import data_containers
from .data_containers import *
from .filegui import InteractiveIO
from . import converter
from . import io
from . import numerics
from . import viewer

__all__ = ['data_containers', 'io', 'viewer', 'converter', 'numerics', 'tests']