from lewis.adapters.stream import StreamInterface, Cmd
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply

SYST_ERR = ";:SYST:ERR?"

@has_log
class Kse4980StreamInterface(StreamInterface):
    
    in_terminator = "\r\n"
    out_terminator = "\n"

    def __init__(self):
        super(Kse4980StreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder(self.catch_all).arg("^#9.*$").build(),  # Catch-all command for debugging
            CmdBuilder(self.get_readings).escape(":FETC?").eos().build(),
            CmdBuilder(self.set_freq).escape(f":FREQ ").float().escape(SYST_ERR).eos().build(),
            CmdBuilder(self.get_freq).escape(":FREQ?").eos().build(),
            CmdBuilder(self.get_curr).escape(":CURR?").eos().build(),
            CmdBuilder(self.get_volt).escape(":VOLT?").eos().build(),
            CmdBuilder(self.set_curr).escape(":CURR ").float().eos().build(),
            CmdBuilder(self.set_volt).escape(":VOLT ").float().eos().build(),
            CmdBuilder(self.get_imprange).escape(":FUNC:IMP:RANG?").eos().build(),
            CmdBuilder(self.set_imprange).escape(":FUNC:IMP:RANG ").float().escape(SYST_ERR).eos().build(),
            CmdBuilder(self.get_autorange).escape(":FUNC:IMP:RANG:AUTO?").eos().build(),
            CmdBuilder(self.set_autorange).escape(":FUNC:IMP:RANG:AUTO ").str().escape(SYST_ERR).eos().build(),
            CmdBuilder(self.get_meas_time_and_avg_factor).escape(":APER?").eos().build(),
            CmdBuilder(self.set_meas_time_and_avg_factor).escape("APER ").str().escape(",").float().escape(SYST_ERR).eos().build(),
            CmdBuilder(self.get_func).escape(":FUNC:IMP?").eos().build(),
            CmdBuilder(self.set_func).escape(":FUNC:IMP ").str().escape(SYST_ERR).eos().build(),
        }

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.errorid = -171
        self.errormsg = "Invalid expression"
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def catch_all(self, command):
        pass

    def _error_str(self):
        return f"{self.device.errorid:+d},{self.device.errormsg}"
    
    def _clear_and_return_error(self):
        self.errorid = 0
        self.errormsg "No error"
        return self._error_str()
    
    def id(self):
        return "Keysight Technologies,E4980AL,MY54413621,B.07.05"

    def get_readings(self):
        return f"{Decimal(self.device.reading1):.5E},{Decimal(self.device.reading2):.5E},+1"

    def get_freq(self):
        return self.device.freq

    def set_freq(self, new_freq):
        self.device.freq = new_freq
        return self._clear_and_return_error()
    
    def get_meas_time_and_avg_factor(self):
        return f"{self.device.meas_time},{self.device.avg_factor}"
    
    def set_meas_time_and_avg_factor(self, meas_time, avg_factor):
        # todoset  error if wrong
        self.device.meas_time = meas_time
        self.device.avg_factor = avg_factor
        return self._clear_and_return_error()
    
    def get_imprange(self):
        return self.device.imprange
    
    def set_imprange(self, new_imprange):
        self.device.imprange = new_imprange
        return self._clear_and_return_error()
    
    def get_autorange(self):
        return 1 if self.device.autorange else 0
    
    def set_autorange(self, new_autorange):
        # todoset  error if wrong
        pass
        return self._clear_and_return_error()

    def get_func(self):
        return self.device.function
    
    def set_func(self, new_func):
        self.device.function = new_func
        return self._clear_and_return_error()
    
    def get_curr(self):
        # check signal type here, and error if in volt mode
        pass

    def get_volt(self):
        # check signal type here, and error if in curr mode
        pass

    def set_curr(self):
        pass

    def set_volt(self):
        pass

        