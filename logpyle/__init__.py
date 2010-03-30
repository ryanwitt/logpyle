#!/usr/bin/env python

import sys

# Attempt to systemwide configuration
try:
    import logpyle_config as config
except ImportError:
    import defaults as config

# Somebody subverted the excepthook already
if sys.excepthook != sys.__excepthook__:
    pass

def excepthook(type, value, traceback):
    sys.__excepthook__(type, value, traceback)

sys.excepthook = excepthook

print __name__


def caller_module_name():
    pass
