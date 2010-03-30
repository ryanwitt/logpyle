#!/usr/bin/env python

import sys

# Attempt to import systemwide configuration
import defaults as config

# Logger identification
import traceback
try:
    name = traceback.extract_stack()[-2][0]
except:
    name = traceback.extract_stack()[-1][0]

print '__name__', __name__
print 'name', name

from logging import *

def _logger():
    return getLogger(name)

for handler, formatter in config.HANDLERS:
    handler.setFormatter(formatter)
    _logger().addHandler(handler)
    getLogger().addHandler(handler)

_logger().propagate = 1
_logger().setLevel(config.LEVEL)
getLogger().setLevel(config.LEVEL)

debug = _logger().debug
info = _logger().info
warning = _logger().warning
error = _logger().error
critical = _logger().critical
log = _logger().log

# Somebody subverted the excepthook already
if sys.excepthook != sys.__excepthook__:
    pass

def excepthook(*args):
    _logger().error(traceback.format_exception(*args))
    sys.__excepthook__(*args)

sys.excepthook = excepthook

