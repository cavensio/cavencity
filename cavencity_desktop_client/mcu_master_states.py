"""
Input (requested) and output (actual) states of the master MCU.
It represents combined state of the master itself and its slaves.
"""


class MasterException(Exception):
    def __init__(self, message):
        self.message = message


class MasterOutputState:
    def __init__(self):
        self.master_uptime: int = 0
        self.master_counter: int = 0
        self.master_backlight: int = 0
        self.slave1_online: bool = False
        self.slave1_uptime: int = 0
        self.slave1_counter: int = 0
        self.slave1_latency: int = 0
        self.slave1_errors: int = 0
        self.slave1_fan_level: int = 0
        self.slave1_light_level: int = 0
        self.slave2_online: bool = False
        self.slave2_uptime: int = 0
        self.slave2_counter: int = 0
        self.slave2_latency: int = 0
        self.slave2_errors: int = 0
        self.slave2_fan_level: int = 0
        self.slave2_light_level: int = 0

    @staticmethod
    def from_mcu_string(mcu_string) -> 'MasterOutputState':
        state = MasterOutputState()
        data = {k: int(v) for k, v in [i.split('=') for i in mcu_string.split(' ')]}
        state.master_uptime = data['mu']
        state.master_counter = data['mc']
        state.master_backlight = data['mbl']
        state.slave1_online = bool(data['s1o'])
        state.slave1_uptime = data['s1u']
        state.slave1_counter = data['s1c']
        state.slave1_latency = data['s1l']
        state.slave1_errors = data['s1e']
        state.slave1_fan_level = data['s1fl']
        state.slave1_light_level = data['s1ll']
        state.slave2_online = bool(data['s2o'])
        state.slave2_uptime = data['s2u']
        state.slave2_counter = data['s2c']
        state.slave2_latency = data['s2l']
        state.slave2_errors = data['s2e']
        state.slave2_fan_level = data['s2fl']
        state.slave2_light_level = data['s2ll']
        return state


class MasterInputState:
    def __init__(self):
        self.master_backlight:int = 0
        self.slave1_fan_level:int = 0
        self.slave1_light_level:int = 0
        self.slave2_fan_level:int = 0
        self.slave2_light_level:int = 0

    def to_mcu_string(self) -> str:
        return ' '.join([
            f'mbl={self.master_backlight}',
            f's1fl={self.slave1_fan_level}',
            f's1ll={self.slave1_light_level}',
            f's2fl={self.slave2_fan_level}',
            f's2ll={self.slave2_light_level}'
        ])
