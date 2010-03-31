#!/usr/bin/env python

import sys

# Attempt to import systemwide configuration
import defaults as config

# Logger identification
import traceback
try:
    # Grab parent module if we can
    name = traceback.extract_stack()[-2][0]
except:
    # Otherwise use our own name
    name = traceback.extract_stack()[-1][0]

print '__name__', __name__
print 'name', name

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

# Somebody subverted the excepthook already
if sys.excepthook != sys.__excepthook__:
    pass

def excepthook(*args):
    _logger().error(traceback.format_exception(*args))
    sys.__excepthook__(*args)

sys.excepthook = excepthook

#try:
#    from cStringIO import StringIO
#except:
#    from StringIO import StringIO
from StringIO import StringIO

class StreamSubverter (StringIO):

    def __init__(self, stream = sys.stdout, logfunc = info, *args, **kwargs):
        self.stream = stream
        self.logfunc = logfunc
        self.stream.write('\nWAKA -- INIT\n')
        return StringIO.__init__(self, *args, **kwargs)

    def flush(self, *args, **kwargs):
        self.stream.flush()
        return StringIO.flush(self, *args, **kwargs)

    def write(self, *args, **kwargs):
        message = self.read()
        self.logfunc(message)
        self.stream.write(message)
        self.stream.write('\nWAKA!\n')
        return StringIO.write(self, *args, **kwargs)
        
_stdout = sys.stdout
out = StreamSubverter(_stdout, logfunc = info)
sys.stdout = out

_stderr = sys.stderr
err = StreamSubverter(_stderr, logfunc = error)
sys.stderr = err

print >>sys.stderr, "Hello!"
