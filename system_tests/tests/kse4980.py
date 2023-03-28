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

    def test_GIVEN_setting_a_current_WHEN_in_voltage_mode_THEN_signal_type_switches(self):
        self.ca.set_pv_value("SIGNALTYPE:SP", "CURR")
        self.ca.assert_that_pv_is("SIGNALTYPE", "CURR")
    
    def test_GIVEN_invalid_function_WHEN_setting_function_THEN_function_is_not_set_and_error_id_populated(self):
        pass

    def test_GIVEN_reset_all_button_pressed_WHEN_non_standard_settings_applied_THEN_defaults_are_restored(self):
        pass

    def test_GIVEN_setting_impedance_range_THEN_imprange_is_updated(self):
        pass

    def test_GIVEN_averaging_factor_set_THEN_averaging_factor_applied_on_device(self):
        pass

    def test_GIVEN_measurement_time_changed_THEN_averaging_factor_and_measurement_time_both_updated(self):
        pass

    def test_GIVEN_both_readings_update_on_device_WHEN_polling_THEN_reading_pvs_updated(self):
        pass

'''
tests
setting curr when volt works and vice versa and switches signal type
setting function wrong does nothing 
reset resets all
impedance setting works 
averaging factor setting updates ok
meas time changing updates ok 
readings gives both readings and both pvs update 

'''