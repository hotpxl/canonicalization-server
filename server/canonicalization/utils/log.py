from __future__ import absolute_import
from __future__ import print_function
import logging


class _Formatter(logging.Formatter):
    def __init__(self):
        datefmt = '%m%d %H:%M:%S'
        super(_Formatter, self).__init__(datefmt=datefmt)

    def get_color(self, level):
        if logging.WARNING <= level:
            return '\x1b[31m'
        elif logging.INFO <= level:
            return '\x1b[32m'
        else:
            return '\x1b[34m'

    def get_label(self, level):
        if level == logging.CRITICAL:
            return 'C'
        elif level == logging.ERROR:
            return 'E'
        elif level == logging.WARNING:
            return 'W'
        elif level == logging.INFO:
            return 'I'
        elif level == logging.DEBUG:
            return 'D'
        else:
            return 'U'

    def format(self, record):
        fmt = self.get_color(record.levelno)
        fmt += self.get_label(record.levelno)
        fmt += '%(asctime)s %(process)d %(filename)s:%(lineno)d:%(funcName)s' \
               ' %(name)s]\x1b[0m'
        fmt += ' %(message)s'
        self._fmt = fmt
        return super(_Formatter, self).format(record)


_handler = logging.StreamHandler()
_handler.setFormatter(_Formatter())


def get_logger(name=None, level=logging.DEBUG):
    logger = logging.getLogger(name)
    if getattr(logger, '_init_done', None):
        return logger
    else:
        logger._init_done = True
        logger.addHandler(_handler)
        logger.setLevel(level)
        return logger
