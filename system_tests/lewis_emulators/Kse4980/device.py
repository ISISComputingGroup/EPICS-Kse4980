from collections import OrderedDict
from .states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedKse4980(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.freq = 0 
        self.function = "CPD"
        self.autorange = False
        self.imprange = 1
        self.volt_mode = True
        self.signallevel = 0
        self.reading1 = 0.0
        self.reading2 = 0.0
        self.errorid = 0 
        self.errormsg = 0
        self.meas_time = "SHOR"
        self.avg_factor = 1

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

