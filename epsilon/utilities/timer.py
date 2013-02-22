from datetime import datetime

from epsilon.logging.logger import Logger
class Timer(object):
    
    def __init__(self, name="Timer", verbose=False):
        self._name = name
        self._start = None
        self._end = None
        self._el = None
        self._verbose = verbose

    def start(self):
        self._start = datetime.now()
        if self._verbose:
            self._timer_print("started at", self._start)

    def stop(self):
        self._stop = datetime.now()

    def elapsed(self):
        if not self._start is None:
            if not self._stop is None:
                self._el = self._stop - self._start
                self._timer_print("time elapsed", self._el)
            else:
                Logger.Log( "%s timer hasn't stopped yet." % self._name )
        else:
            Logger.Log( "%s timer hasn't started yet." % self._name )

    def _timer_print(self, message, time):
        pt = time.seconds + (time.microseconds / 1000000.0 )
        Logger.Log( "%s timer %s: %4.4f" % ( self._name, message, pt) )