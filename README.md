
logpyle - logging for lazy programmers
======================================

Logpyles are full of snakes.

Features:

 - Drop-in replacement for the python `logging` module
 - Turns uncaught exceptions into log entries
 - Intelligently turns program output into log entries (for when you lack the energy to put in logging right away, or you are trying to tame a program not built with logging)

Future features:

 - Provide useful hooks
 - Support multiple processes

Logpyle came about so I could tame the output from a large pile of loosely associated python programs.

## How to use it

    import logpyle

Do this in each python file you want to log.

To get more fancy, logpyle can replace python's `logging` module:

    import logpyle as logging
    # Do whatever you normally do with the logging module

## Configuring

Global config is taken care of by writing a `logpyle_config` module and putting it in your python path so that logpyle sees it when you are importing logpyle.

Here is an example `logpyle_config.py` that redirects messages to the syslog:

    import logging
    from logging.handlers import SysLogHandler
    
    syslog = SysLogHandler('/var/run/syslog', SysLogHandler.LOG_USER)
    syslog.setFormatter(logging.Formatter('%(name)s %(levelname)s: %(message)s'))
    
    HANDLERS = (syslog,)
    
    LEVEL = logging.DEBUG

### Local config

You can override the global configs by importing the `logpyle_config` module and changing settings from the defaults:

    import logpyle_config
    logpyle_config.SUBVERT_IO = False
     

### Config options

 - `HANDLERS` -- A list of log handlers that you want to see the log events. Take a look at python's `logging.handlers`.
 - `LEVEL` (default `logging.DEBUG`) -- Global log level. Your handlers will accept events of this significance or higher.
 - `SUBVERT_EXCEPTHOOK` (default `True`) -- Catch uncaught exceptions and logg them at the `logging.ERROR` level
 - `SUBVERT_IO` (default `True`) -- Log lines from `sys.stdout` and `sys.stderr`
 - `STDOUT_LEVEL` (default `logging.INFO`) -- Log level for `sys.stdout`
 - `STDERR_LEVEL` (default `logging.ERROR`) -- Log level for `sys.stderr`



