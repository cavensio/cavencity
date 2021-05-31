import unittest

from mcu_master_states import MasterSlaveTargetState, MasterSlaveActualState


class TestMasterSlaveTargetState(unittest.TestCase):
    def test_to_mcu_string(self):
        state = MasterSlaveTargetState()
        state.masterState.backlight = 5
        state.slaveStates[0].fan_level = 3
        state.slaveStates[0].light_level = 4
        state.slaveStates[1].fan_level = 1
        state.slaveStates[1].light_level = 2

        self.assertEquals(state.to_mcu_string(), 'mbl=5 s1fl=3 s1ll=4 s2fl=1 s2ll=2')


class TestMasterOutputState(unittest.TestCase):
    def test_from_mcu_string(self):
        state = MasterSlaveActualState.from_mcu_string(
            'mu=112233 mc=456 mbl=7 '
            's1o=1 s1u=1234 s1c=42 s1l=1982 s1e=345 s1fl=16 s1ll=17 '
            's2o=0 s2u=2345 s2c=53 s2l=8765 s2e=987 s2fl=28 s2ll=29'
        )
        self.assertEqual(state.masterState.uptime, 112233)
        self.assertEqual(state.masterState.counter, 456)
        self.assertEqual(state.masterState.backlight, 7)

        self.assertTrue(state.slaveStates[0].online)
        self.assertEqual(state.slaveStates[0].uptime, 1234)
        self.assertEqual(state.slaveStates[0].counter, 42)
        self.assertEqual(state.slaveStates[0].latency, 1982)
        self.assertEqual(state.slaveStates[0].errors, 345)
        self.assertEqual(state.slaveStates[0].fan_level, 16)
        self.assertEqual(state.slaveStates[0].light_level, 17)

        self.assertFalse(state.slaveStates[1].online)
        self.assertEqual(state.slaveStates[1].uptime, 2345)
        self.assertEqual(state.slaveStates[1].counter, 53)
        self.assertEqual(state.slaveStates[1].latency, 8765)
        self.assertEqual(state.slaveStates[1].errors, 987)
        self.assertEqual(state.slaveStates[1].fan_level, 28)
        self.assertEqual(state.slaveStates[1].light_level, 29)
