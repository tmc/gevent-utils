import time
import mock
import gevent
from unittest import TestCase

from gevent_utils import BlockingDetector


class TestBlockingDetector(TestCase):

    @mock.patch.object(BlockingDetector, 'alarm_handler')
    def test_triggered(self, mock_alarm_handler):
        detector = BlockingDetector(2)
        gevent.spawn(detector)
        gevent.sleep()

        self.assertFalse(mock_alarm_handler.called)
        time.sleep(1)
        self.assertFalse(mock_alarm_handler.called)
        time.sleep(1)

        # after two seconds of sleep the alarm_handler should have been called
        self.assertTrue(mock_alarm_handler.called)
