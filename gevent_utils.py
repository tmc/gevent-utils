"""
gevent-utils
============

Debugging utilities for gevent.
"""
import math
import signal
import traceback
import gevent
import logging

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

class BlockingDetector(object):
    """
    Utility class to detect thread blocking. Intended for debugging only.
    
    ``blocking_resolution`` is the number of seconds to wait before considering
    the thread blocked.
    
    Operates by setting and attempt to clearing an alarm signal. If it does not
    clear the alarm signal then the thread is likely blocked and
    ``BlockingDetector.alarm_handler`` is invoked with the signal and current
    frame. The default implementation prints the stack from the blocked frame
    with logging.error.
    
    Invoke via: gevent.spawn(BlockingDetector())
    """
    def __init__(self, blocking_resolution=1):
        self.blocking_resolution = blocking_resolution

    def __call__(self):
        """
        Loop for 95% of our detection time and attempt to clear the signal.
        """
        while True:
            self.set_signal()
            gevent.sleep(self.blocking_resolution * 0.95)
            self.clear_signal()

    def alarm_handler(self, signum, frame):
        logging.error('Blocking detector ALARMED:\n' + '\n'.join(traceback.format_stack(frame)))

    def set_signal(self):
        tmp = signal.signal(signal.SIGALRM, self.alarm_handler)
        if tmp != self.alarm_handler:
            self._old_signal_handler = tmp
        arm_alarm(self.blocking_resolution)

    def clear_signal(self, resolution):
        if (hasattr(self, "_old_signal_handler") and self._old_signal_handler):
            signal.signal(signal.SIGALRM, self._old_signal_handler)
        signal.alarm(0)

