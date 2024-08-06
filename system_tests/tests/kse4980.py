import unittest

from parameterized import parameterized
from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.test_modes import TestModes
from utils.testing import get_running_lewis_and_ioc, parameterized_list

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
        invalid_function = "blah"
        self.ca.set_pv_value("FUNC:SP", invalid_function)
        self.ca.assert_that_pv_is_not("FUNC", invalid_function)
        self.ca.assert_that_pv_is("ERRORID", -171)

    def test_GIVEN_reset_all_button_pressed_WHEN_non_standard_settings_applied_THEN_defaults_are_restored(self):
        self.ca.set_pv_value("FUNC:SP", "CPG")
        self.ca.set_pv_value("AUTORANGE:SP", "ON")
        self.ca.assert_that_pv_is("FUNC", "CPG")
        self.ca.assert_that_pv_is("AUTORANGE", "ON")
        self.ca.set_pv_value("RESET", 1)
        self.ca.assert_that_pv_is("FUNC", "CPD")
        self.ca.assert_that_pv_is("AUTORANGE", "OFF")

    def test_GIVEN_setting_impedance_range_THEN_imprange_is_updated(self):
        setpoint = "10k"
        self.ca.set_pv_value("IMPRANGE:SP", setpoint)
        self.ca.assert_that_pv_is("IMPRANGE", setpoint)

    def test_GIVEN_meas_time_and_averaging_factor_set_THEN_both_applied_on_device(self):
        meas_time_sp = "MED"
        avg_fact_sp = 22
        self.ca.set_pv_value("MEAS_TIME:SP", meas_time_sp)
        self.ca.set_pv_value("AVG_FACTOR:SP", avg_fact_sp)

        self.ca.assert_that_pv_is("MEAS_TIME", meas_time_sp)
        self.ca.assert_that_pv_is("AVG_FACTOR", avg_fact_sp)

    def test_GIVEN_averaging_factor_changed_only_THEN_averaging_factor_and_measurement_time_both_updated(self):
        avg_fact_sp = 23
        self.ca.set_pv_value("AVG_FACTOR:SP", avg_fact_sp)
        self.ca.assert_that_pv_is("AVG_FACTOR", avg_fact_sp)

    def test_GIVEN_both_readings_update_on_device_WHEN_polling_THEN_reading_pvs_updated(self):
        reading1 = 1.123
        reading2 = 2.234
        self._lewis.backdoor_set_on_device("reading1", reading1)
        self._lewis.backdoor_set_on_device("reading2", reading2)

        self.ca.assert_that_pv_is("PRIMARY", reading1)
        self.ca.assert_that_pv_is("SECONDARY", reading2)
    
    @parameterized.expand(parameterized_list([
        ("CPD", "F", ""),
        ("RX", "Ohms", "Ohms"),
        ("VDID", "V", "A"),
        ("LPRP", "H", "Ohms"),
        ("CPG", "F", "S"),
    ]))
    def test_GIVEN_function_changed_THEN_correct_engineering_units_are_applied_to_readings(self, _, new_func, expected_first_unit, expected_second_unit):
        self.ca.set_pv_value("FUNC:SP", new_func)
        self.ca.assert_that_pv_is("PRIMARY.EGU", expected_first_unit)
        self.ca.assert_that_pv_is("SECONDARY.EGU", expected_second_unit)


    @parameterized.expand(parameterized_list([
        ("CURR", 0.2),
        ("VOLT", 21),
    ]))
    def test_GIVEN_signallevel_set_too_high_WHEN_setting_level_THEN_error_propagates(self, _, signaltype, over_limit):
        self.ca.set_pv_value("SIGNALTYPE:SP", signaltype)

        self.ca.set_pv_value("SIGNALLEVEL:SP", over_limit)

        self.ca.assert_that_pv_is_not("ERRORID", 0)
        self.ca.assert_that_pv_is_not("SIGNALLEVEL", over_limit)
