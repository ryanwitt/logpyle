
import logging
from logging.handlers import SysLogHandler

syslog = SysLogHandler('/var/run/syslog', SysLogHandler.LOG_USER)
syslog.setFormatter(logging.Formatter('%(name)s %(levelname)s: %(message)s'))

HANDLERS = (syslog,)

LEVEL = logging.DEBUG
