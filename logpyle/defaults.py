#!/usr/bin/env python

import logging

HANDLERS = []
LEVEL = logging.ERROR
    
try:
    from logpyle_config import *
except ImportError:
    pass
