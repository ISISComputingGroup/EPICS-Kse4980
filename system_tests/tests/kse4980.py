import unittest

from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.test_modes import TestModes
from utils.testing import get_running_lewis_and_ioc, skip_if_recsim


DEVICE_PREFIX = "KSE4980_01"


IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("KSE4980"),
        "macros": {},
        "emulator": "Kse4980",
    },
]


TEST_MODES = [TestModes.DEVSIM]


class Kse4980Tests(unittest.TestCase):
    """
    Tests for the Kse4980 IOC.
    """
    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc("Kse4980", DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX, default_wait_time=0.0)

    def test_that_fails(self):
        self.fail("You haven't implemented any tests!")
