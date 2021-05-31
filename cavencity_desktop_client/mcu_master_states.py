"""
Input (requested) and output (actual) states of the master MCU.
It represents combined state of the master itself and its slaves.
"""


class MasterException(Exception):
    def __init__(self, message):
        self.message = message


class SlaveActualState:
    def __init__(self):
        self.online: bool = False
        self.uptime: int = 0
        self.counter: int = 0
        self.latency: int = 0
        self.errors: int = 0
        self.fan_level: int = 0
        self.light_level: int = 0


class MasterActualState:
    def __init__(self):
        self.online: bool = False
        self.uptime: int = 0
        self.counter: int = 0
        self.latency: int = 0
        self.errors: int = 0
        self.backlight: int = 0


class MasterSlaveActualState:
    def __init__(self):
        self.masterState: MasterActualState = MasterActualState()
        self.slaveStates: list[SlaveActualState] = [SlaveActualState(), SlaveActualState()]

    @staticmethod
    def from_mcu_string(mcu_string) -> 'MasterSlaveActualState':
        state = MasterSlaveActualState()
        data = {k: int(v) for k, v in [i.split('=') for i in mcu_string.split(' ')]}
        state.masterState.uptime = data['mu']
        state.masterState.counter = data['mc']
        state.masterState.backlight = data['mbl']

        state.slaveStates[0].online = bool(data['s1o'])
        state.slaveStates[0].uptime = data['s1u']
        state.slaveStates[0].counter = data['s1c']
        state.slaveStates[0].latency = data['s1l']
        state.slaveStates[0].errors = data['s1e']
        state.slaveStates[0].fan_level = data['s1fl']
        state.slaveStates[0].light_level = data['s1ll']

        state.slaveStates[1].online = bool(data['s2o'])
        state.slaveStates[1].uptime = data['s2u']
        state.slaveStates[1].counter = data['s2c']
        state.slaveStates[1].latency = data['s2l']
        state.slaveStates[1].errors = data['s2e']
        state.slaveStates[1].fan_level = data['s2fl']
        state.slaveStates[1].light_level = data['s2ll']
        return state


class MasterTargetState:
    def __init__(self):
        self.backlight: int = 0


class SlaveTargetState:
    def __init__(self):
        self.fan_level: int = 0
        self.light_level: int = 0


class MasterSlaveTargetState:
    def __init__(self):
        self.masterState: MasterTargetState = MasterTargetState()
        self.slaveStates: list[SlaveTargetState] = [SlaveTargetState(), SlaveTargetState()]

    def to_mcu_string(self) -> str:
        return ' '.join([
            f'mbl={self.masterState.backlight}',
            f's1fl={self.slaveStates[0].fan_level}',
            f's1ll={self.slaveStates[0].light_level}',
            f's2fl={self.slaveStates[1].fan_level}',
            f's2ll={self.slaveStates[1].light_level}'
        ])
