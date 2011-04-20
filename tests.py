import time
import mock
import gevent
from unittest import TestCase

from gevent_utils import BlockingDetector, AlarmInterrupt

class TestBlockingDetector(TestCase):

    @mock.patch.object(BlockingDetector, 'alarm_handler')
    def test_triggered_when_blocking(self, mock_alarm_handler):
        detector_greenlet = gevent.spawn(BlockingDetector(2))
        gevent.sleep()

        self.assertFalse(mock_alarm_handler.called)
        time.sleep(1)
        self.assertFalse(mock_alarm_handler.called)
        time.sleep(1)

        # after two seconds of sleep the alarm_handler should have been called
        self.assertTrue(mock_alarm_handler.called)
        detector_greenlet.kill()

    def test_actual_exception_raised(self):
        detector_greenlet = gevent.spawn(BlockingDetector())
        gevent.sleep()

        self.assertRaises(AlarmInterrupt, time.sleep, 1)
        detector_greenlet.kill()

    @mock.patch.object(BlockingDetector, 'alarm_handler')
    def test_not_triggered_when_cooperating(self, mock_alarm_handler):
        detector_greenlet = gevent.spawn(BlockingDetector())
        gevent.sleep()

        self.assertFalse(mock_alarm_handler.called)
        gevent.sleep(2)
        self.assertFalse(mock_alarm_handler.called)
        detector_greenlet.kill()
