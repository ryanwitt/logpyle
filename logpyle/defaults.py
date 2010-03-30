#!/usr/bin/env python

import logging

LOGDIR = '/var/log/logpyle'

LOGFILE = '/var/log/logpyle.log'

from logging.handlers import SysLogHandler
HANDLERS = (
    (
        SysLogHandler('/var/run/log', SysLogHandler.LOG_USER),
        logging.Formatter('%(name)s %(levelname)s: %(message)s')
    ),
)

LEVEL = logging.DEBUG
    
try:
    from logpyle_config import *
except ImportError:
    pass
