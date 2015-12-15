"""Customizing import behavior on imported modules"""
# author: Deagels
#
# Usage: in the importing module (i.e main) "import pimport" is enough.
# All subsequent imports will look for and run two magic functions in the
# global scope on the imported modules; __new__ and __init__
#
# __new__ if defined, is responsible for returning the object to be
# imported, this can be of any arbitrary type
# __init__ is called afterwards, not on the object returned, but the
# module.
# both functions take two arguments:
# 1. module/self which is the module the functions are defined in
# 2. caller/requester which is the module importing

import sys
import inspect

from importlib import _bootstrap # evil hacks

inner_fal = _bootstrap._find_and_load
def _find_and_load(name, import_):
    pimpname = "pimp$"+ name
    module = sys.modules[pimpname] if pimpname in sys.modules \
        else inner_fal(name, import_)
    caller = caller_module()
    mod    = module
    if "__new__" in mod.__dict__:
        module = mod.__new__(mod, caller)
    if "__init__" in mod.__dict__:
        mod.__init__(mod, caller)
    # remove cache in order to force us back here again next import
    del sys.modules[name] 
    return module
_bootstrap._find_and_load = _find_and_load

def caller_module():
    try: name = inspect.currentframe().f_back.f_back.f_globals["__name__"]
    except KeyError: raise ValueError("__name__ is not in the global namespace")
    try: return sys.modules[name]
    except KeyError: raise ValueError("Cannot find module named '%s' in sys.modules. Have __name__ been modified?" % name)
