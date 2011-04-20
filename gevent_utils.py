"""
gevent-utils
============

Debugging utilities for gevent.
"""
import math
import signal
import gevent

arm_alarm = None
if hasattr(signal, 'setitimer'):
    def alarm_itimer(seconds):
        signal.setitimer(signal.ITIMER_REAL, seconds)
    arm_alarm = alarm_itimer
else:
    try:
        import itimer
        arm_alarm = itimer.alarm
    except ImportError:
        def alarm_signal(seconds):
            signal.alarm(math.ceil(seconds))
        arm_alarm = alarm_signal

class AlarmInterrupt(BaseException): pass

class BlockingDetector(object):
    """
    Utility class to detect thread blocking. Intended for debugging only.
    
    ``timeout`` is the number of seconds to wait before considering the thread
    blocked.
    
    Operates by setting and attempt to clear an alarm signal. The alarm signal
    cannot be cleared then the thread is considered blocked and
    ``BlockingDetector.alarm_handler`` is invoked with the signal and current
    frame. An ``AlarmInterrupt`` exception will be raised if the signal
    actually gets raised.
    
    Invoke via: gevent.spawn(BlockingDetector())
    """
    def __init__(self, timeout=1):
        self.timeout = timeout

    def __call__(self):
        """
        Loop for 95% of our detection time and attempt to clear the signal.
        """
        while True:
            self.set_signal()
            gevent.sleep(self.timeout * 0.95)
            self.clear_signal()
            # sleep the rest of the time
            gevent.sleep(self.timeout * 0.05)

    def alarm_handler(self, signum, frame):
        raise AlarmInterrupt('Blocking detected')

    def set_signal(self):
        tmp = signal.signal(signal.SIGALRM, self.alarm_handler)
        if tmp != self.alarm_handler:
            self._old_signal_handler = tmp
        arm_alarm(self.timeout)

    def clear_signal(self):
        if (hasattr(self, "_old_signal_handler") and self._old_signal_handler):
            signal.signal(signal.SIGALRM, self._old_signal_handler)
        signal.alarm(0)

