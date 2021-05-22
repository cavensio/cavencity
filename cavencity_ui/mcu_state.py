"""
Input (requested) and output (actual) states of the MCUs network.
It represents the aggregated state of all units in the network.
"""


class OutputState:
    def __init__(self):
        self.master_uptime: int = 0
        self.master_counter: int = 0
        self.master_light_intensity: int = 0
        self.slave1_online: bool = False
        self.slave1_uptime: int = 0
        self.slave1_counter: int = 0
        self.slave1_fan_speed: int = 0
        self.slave1_light_intensity: int = 0
        self.slave2_online: bool = False
        self.slave2_uptime: int = 0
        self.slave2_counter: int = 0
        self.slave2_fan_speed: int = 0
        self.slave2_light_intensity: int = 0

    @staticmethod
    def from_mcu_string(mcu_string) -> 'OutputState':
        state = OutputState()
        data = {k: int(v) for k, v in [i.split('=') for i in mcu_string.split(',')]}
        state.master_uptime = data['mu']
        state.master_counter = data['mc']
        state.master_light_intensity = data['mli']
        state.slave1_online = data['s1o']
        state.slave1_uptime = data['s1u']
        state.slave1_counter = data['s1c']
        state.slave1_fan_speed = data['s1fs']
        state.slave1_light_intensity = data['s1li']
        state.slave2_online = data['s2o']
        state.slave2_uptime = data['s2u']
        state.slave2_counter = data['s2c']
        state.slave2_fan_speed = data['s2fs']
        state.slave2_light_intensity = data['s2li']
        return state


class InputState:
    def __init__(self, master_light_intensity: int,
                 slave1_fan_speed: int, slave1_light_intensity: int,
                 slave2_fan_speed: int, slave2_light_intensity: int
                 ):
        self.master_light_intensity = master_light_intensity
        self.slave1_fan_speed = slave1_fan_speed
        self.slave1_light_intensity = slave1_light_intensity
        self.slave2_fan_speed = slave2_fan_speed
        self.slave2_light_intensity = slave2_light_intensity

    def to_mcu_string(self) -> str:
        return ','.join([
            f'mli={self.master_light_intensity}',
            f's1fs={self.slave1_fan_speed}',
            f's1li={self.slave1_light_intensity}',
            f's2fs={self.slave2_fan_speed}',
            f's2li={self.slave2_light_intensity}'
        ])
