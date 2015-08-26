
# -*- coding: utf-8 -*-
## @package guided_filter.util.timer
#
#  Timer utility package.
#  @author      tody
#  @date        2015/07/29

import time


class Timer(object):
    def __init__(self, timerName, logger=None):
        self.name = timerName
        self.logger = logger

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs

        self.secStr = "%s: %f s" % (self.name, self.secs)
        self.msecStr = "%s: %f ms" % (self.name, self.msecs)

        if self.logger is not None:
            self.logger.debug(self.secStr)

        else:
            print self.secStr

    def __str__(self):
        return self.secStr


def timing_func(func=None, timerName=None, logger=None):
    def _decorator(func):
        _timerName = timerName
        if timerName is None:
            _timerName = func.__name__

        import functools

        @functools.wraps(func)
        def _with_timing(*args, **kwargs):

            with Timer(_timerName, logger) as t:
                ret = func(*args, **kwargs)

            return ret
        return _with_timing

    if func:
        return _decorator(func)
    else:
        return _decorator
