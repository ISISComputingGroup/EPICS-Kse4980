from lewis.adapters.stream import StreamInterface, Cmd
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply


@has_log
class Kse4980StreamInterface(StreamInterface):
    
    in_terminator = "\r\n"
    out_terminator = "\n"

    def __init__(self):
        super(Kse4980StreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder(self.catch_all).arg("^#9.*$").build(),  # Catch-all command for debugging
            CmdBuilder(self.get_readings).escape(":FETC?").eos().build()
        }

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def catch_all(self, command):
        pass
    
    def get_readings(self):
        return f"{Decimal(self.device.reading1):.2E},{Decimal(self.device.reading2):.2E},+1"

    def get_freq(self):
        return self.device.freq

    def set_freq(self, new_freq):
        self.device.freq = new_freq
    
    def get_meas_time_and_avg_factor(self):
        return f"{self.device.meas_time},{self.device.avg_factor}"
    
    def set_meas_time_and_avg_factor(self, meas_time, avg_factor):
        # todoset  error if wrong
        self.device.meas_time = meas_time
        self.device.avg_factor = avg_factor
    
    def get_imprange(self):
        return self.device.imprange
    
    def set_imprange(self, new_imprange):
        self.device.imprange = new_imprange
    
    def get_autorange(self):
        return 1 if self.device.autorange else 0
    
    def set_autorange(self, new_autorange):
        # todoset  error if wrong
        pass

    def get_func(self):
        return self.device.function
    
    def set_func(self, new_func):
        self.device.function = new_func
    

        