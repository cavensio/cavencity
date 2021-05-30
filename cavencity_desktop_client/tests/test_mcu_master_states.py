import unittest

from mcu_master_states import MasterInputState, MasterOutputState


class TestMasterInputState(unittest.TestCase):
    def test_to_mcu_string(self):
        input_state = MasterInputState()
        input_state.master_backlight = 5
        input_state.slave1_fan_level = 3
        input_state.slave1_light_level = 4
        input_state.slave2_fan_level = 1
        input_state.slave2_light_level = 2

        self.assertEquals(input_state.to_mcu_string(), 'mb=5 s1fl=3 s1ll=4 s2fl=1 s2ll=2')


class TestMasterOutputState(unittest.TestCase):
    def test_from_mcu_string(self):
        output_state = MasterOutputState.from_mcu_string(
            'mu=112233 mc=456 mb=7 '
            's1o=1 s1u=1234 s1c=42 s1l=1982 s1e=345 s1fl=16 s1ll=17 '
            's2o=0 s2u=2345 s2c=53 s2l=8765 s2e=987 s2fl=28 s2ll=29'
        )
        self.assertEqual(output_state.master_uptime, 112233)
        self.assertEqual(output_state.master_counter, 456)
        self.assertEqual(output_state.master_backlight, 7)

        self.assertTrue(output_state.slave1_online)
        self.assertEqual(output_state.slave1_uptime, 1234)
        self.assertEqual(output_state.slave1_counter, 42)
        self.assertEqual(output_state.slave1_latency, 1982)
        self.assertEqual(output_state.slave1_errors, 345)
        self.assertEqual(output_state.slave1_fan_level, 16)
        self.assertEqual(output_state.slave1_light_level, 17)

        self.assertFalse(output_state.slave2_online)
        self.assertEqual(output_state.slave2_uptime, 2345)
        self.assertEqual(output_state.slave2_counter, 53)
        self.assertEqual(output_state.slave2_latency, 8765)
        self.assertEqual(output_state.slave2_errors, 987)
        self.assertEqual(output_state.slave2_fan_level, 28)
        self.assertEqual(output_state.slave2_light_level, 29)
