
# -*- coding: utf-8 -*-
## @package guided_filter.util.timer
#
#  Timer utility package.
#  @author      tody
#  @date        2015/07/29

import time


class Timer(object):
    def __init__(self, timer_name="", output=False, logger=None):
        self._name = timer_name
        self._logger = logger
        self._output = output
        self._end_time = None
        self.start()

    def start(self):
        self._start_time = time.time()

    def stop(self):
        self._end_time = time.time()

    def seconds(self):
        if self._end_time is None:
            self.stop()
        return self._end_time - self._start_time

    def milliseconds(self):
        return self.seconds() * 1000  # millisecs

    def _secondsStr(self):
        return "%s: %f s" % (self._name, self.seconds())

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

        if self._logger is not None:
            self._logger.debug(self._secondsStr())

        if self._output:
            print self._secondsStr()

    def __str__(self):
        return self._secondsStr()


def timing_func(func=None, timer_name=None, logger=None):
    def _decorator(func):
        _timerName = timer_name
        if timer_name is None:
            _timerName = func.__name__

        import functools

        @functools.wraps(func)
        def _with_timing(*args, **kwargs):

            with Timer(_timerName, output=True, logger=logger) as t:
                ret = func(*args, **kwargs)

            return ret
        return _with_timing

    if func:
        return _decorator(func)
    else:
        return _decorator
