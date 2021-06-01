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
        state.masterState.uptime = data.get('mu', 0)
        state.masterState.counter = data.get('mc', 0)
        state.masterState.backlight = data.get('mbl', 0)

        state.slaveStates[0].online = bool(data.get('s1o', 0))
        state.slaveStates[0].uptime = data.get('s1u', 0)
        state.slaveStates[0].counter = data.get('s1c', 0)
        state.slaveStates[0].latency = data.get('s1l', 0)
        state.slaveStates[0].errors = data.get('s1e', 0)
        state.slaveStates[0].fan_level = data.get('s1fl', 0)
        state.slaveStates[0].light_level = data.get('s1ll', 0)

        state.slaveStates[1].online = bool(data.get('s2o', 0))
        state.slaveStates[1].uptime = data.get('s2u', 0)
        state.slaveStates[1].counter = data.get('s2c', 0)
        state.slaveStates[1].latency = data.get('s2l', 0)
        state.slaveStates[1].errors = data.get('s2e', 0)
        state.slaveStates[1].fan_level = data.get('s2fl', 0)
        state.slaveStates[1].light_level = data.get('s2ll', 0)
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
