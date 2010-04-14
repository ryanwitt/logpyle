#!/usr/bin/env python

import logging

HANDLERS = []
LEVEL = logging.ERROR
    
SUBVERT_EXCEPTHOOK = True

SUBVERT_IO = True
STDOUT_LEVEL = logging.INFO
STDERR_LEVEL = logging.ERROR

try:
    from logpyle_config import *
except ImportError:
    pass
