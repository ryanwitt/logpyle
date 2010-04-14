#!/usr/bin/env python

#
# Emulate the logging module
#

import logging
__all__ = logging.__all__

#
# Systemwide logpyle configuration
#
# The defaults module imports the user-level config module which
# is called `logpyle_config`
#

import defaults as config

#
# Module identification
#
# Attempt to discover the identity of our parent module and use
# it as our logger name
#

import traceback
try:
    # Grab parent module if we can
    name = traceback.extract_stack()[-2][0]
except:
    # Otherwise use our own name
    name = traceback.extract_stack()[-1][0]

# Logger setup

from logging import *
from logging import getLogger

def _logger():
    return getLogger(name)

for handler in config.HANDLERS:
    #_logger().addHandler(handler)
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


import sys

#
# Exception hook
#
# Log errors
#

if config.SUBVERT_EXCEPTHOOK:

    # Somebody subverted the excepthook already!
    # We'll just stomp on them for now.
    if sys.excepthook != sys.__excepthook__:
        pass

    def excepthook(*args):
        _logger().error(
            repr(
                ''.join(
                    traceback.format_exception(*args)
                )
            )
        )
        sys.__excepthook__(*args)

    sys.excepthook = excepthook

#
# stdout/stderr subversion
#
# We want to grab everything the program sends and automatically
# log it. Controlled by various config variables.
#
# Decision: capture sys.stdout and sys.stderr rather than being
# being clever with dup2 at the moment because that may have
# some unintended consequences. Can revisit this if performance
# becomes an issue (users can also turn feature off).
#

if config.SUBVERT_IO:

    # No cStringIO here because we need to subclass it
    from StringIO import StringIO

    class StreamSubverter (StringIO):

        def __init__(
            self, 
            stream = sys.stdout, 
            loglevel = info, 
            *args, 
            **kwargs
        ):
            self.stream = stream
            self.loglevel = loglevel
            return StringIO.__init__(self, *args, **kwargs)

        def flush(self, *args, **kwargs):

            # Grab the message we've built up so far
            message = StringIO.seek(self, 0)
            message = StringIO.read(self)

            # And erase the buffer
            StringIO.seek(self, 0)
            StringIO.truncate(self)

            # Now log all of the lines we've built up
            for line in message.strip('\n').split('\n'):
                log(self.loglevel, line)

            # And echo out the lines to the subvertee
            self.stream.write(message)
            self.stream.flush()

        def write(self, message, *args, **kwargs):

            # Make sure we are dealing with strings
            if not isinstance(message, basestring):
                message = str(message)

            # Buffer the write we got for flush later
            StringIO.write(self, message)

            # Right now, flush according to the simple rule
            # that every newline triggers a flush
            if message.endswith('\n'):
                self.flush()
        
        def close(self):
            
            # Make sure we git rid of buffered data if we're closing
            self.stream.flush()
            StringIO.close(self)

    # Do the dirty work
    _stdout = sys.stdout
    out = StreamSubverter(_stdout, loglevel = config.STDOUT_LEVEL)
    sys.stdout = out

    _stderr = sys.stderr
    err = StreamSubverter(_stderr, loglevel = config.STDERR_LEVEL)
    sys.stderr = err

