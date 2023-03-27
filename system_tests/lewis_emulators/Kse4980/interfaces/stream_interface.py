from lewis.adapters.stream import StreamInterface, Cmd
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply
from decimal import Decimal 
SYST_ERR = ";:SYST:ERR?"

@has_log
class Kse4980StreamInterface(StreamInterface):
    
    in_terminator = "\r\n"
    out_terminator = "\n"

    def __init__(self):
        super(Kse4980StreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder(self.get_readings).escape(":FETC?").eos().build(),
            CmdBuilder(self.set_freq).escape(":FREQ ").float().escape(SYST_ERR).eos().build(),
            CmdBuilder(self.get_freq).escape(":FREQ?").eos().build(),
            CmdBuilder(self.get_curr).escape(":CURR?").eos().build(),
            CmdBuilder(self.get_volt).escape(":VOLT?").eos().build(),
            CmdBuilder(self.set_curr).escape(":CURR ").float().escape(SYST_ERR).eos().build(),
            CmdBuilder(self.set_volt).escape(":VOLT ").float().escape(SYST_ERR).eos().build(),
            CmdBuilder(self.get_imprange).escape(":FUNC:IMP:RANG?").eos().build(),
            CmdBuilder(self.set_imprange).escape(":FUNC:IMP:RANG ").arg("0.1|1|10|100|300|1000|3000|10000|30000|100000").escape(SYST_ERR).eos().build(),
            CmdBuilder(self.get_autorange).escape(":FUNC:IMP:RANG:AUTO?").eos().build(),
            CmdBuilder(self.set_autorange).escape(":FUNC:IMP:RANG:AUTO ").arg("1|0").escape(SYST_ERR).eos().build(),
            CmdBuilder(self.get_meas_time_and_avg_factor).escape(":APER?").eos().build(),
            CmdBuilder(self.set_meas_time_and_avg_factor).escape("APER ").arg("SHOR|MED|LONG").escape(",").float().escape(SYST_ERR).eos().build(),
            CmdBuilder(self.get_func).escape(":FUNC:IMP?").eos().build(),
            CmdBuilder(self.set_func).escape(":FUNC:IMP ").arg("CPD|CPQ|CPG|CPRP|CSD|CSQ|CSRS|LPD|LPQ|LPG|LPRP|LPRD|LSD|LSQ|LSRS|LSRD|RX|ZTD|ZTR|GB|YTD|YTR|VDID").escape(SYST_ERR).eos().build(),
            CmdBuilder(self.reset_device).escape(":*RST;*CLS;:INIT;").eos().build(),
            CmdBuilder(self.init_device).escape(":INIT;").eos().build(),
            CmdBuilder(self.id).escape("*IDN?").eos().build()
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
    
    def reset_device(self):
        self.device._initialize_data()
    
    def init_device(self):
        pass

    def _error_str(self):
        return f"{self.device.errorid:+d},{self.device.errormsg}"
    
    def _clear_and_return_error(self):
        self.errorid = 0
        self.errormsg = "No error"
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
        self.device.meas_time = meas_time
        self.device.avg_factor = avg_factor
        return self._clear_and_return_error()
    
    def get_imprange(self):
        # Yuck, the device always returns xE{+,-}0y where y is the exponent.
        # There doesn't seem to be a nice way of doing this with the python format chars
        imprange_full = f"{Decimal(self.device.imprange):+.5E}"
        imprange_exp_stripped = imprange_full[:-1]
        exponent = imprange_full[-1:]
        return f"{imprange_exp_stripped}0{exponent}"
    
    def set_imprange(self, new_imprange):
        self.device.imprange = new_imprange
        return self._clear_and_return_error()
    
    def get_autorange(self):
        return 1 if self.device.autorange is True else 0
    
    def set_autorange(self, new_autorange):
        self.device.autorange = True if int(new_autorange) == 1 else False
        return self._clear_and_return_error()

    def get_func(self):
        return self.device.function
    
    def set_func(self, new_func):
        self.device.function = new_func
        return self._clear_and_return_error()
    
    def get_curr(self):
        # check signal type here, and error if in volt mode
        return "" if self.device.volt_mode else self.device.signallevel

    def get_volt(self):
        # check signal type here, and error if in curr mode
        return "" if not self.device.volt_mode else self.device.signallevel

    def set_curr(self, new_curr):
        self.device.volt_mode = False
        self.device.signallevel = new_curr
        return self._clear_and_return_error()

    def set_volt(self, new_volt):
        self.device.volt_mode = True
        self.device.signallevel = new_volt
        return self._clear_and_return_error()


        