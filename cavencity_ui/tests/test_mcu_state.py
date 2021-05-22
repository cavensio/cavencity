import unittest

from mcu_state import InputState, OutputState


class TestInputState(unittest.TestCase):
    def test_to_mcu_string(self):
        input_state = InputState(5, 3, 4, 1, 2)
        self.assertEquals('mb=5 s1f=3 s1l=4 s2f=1 s2l=2', input_state.to_mcu_string())


class TestOutputState(unittest.TestCase):
    def test_from_mcu_string(self):
        output_state = OutputState.from_mcu_string(
            'mu=112233 mc=456 mb=7 s1o=1 s1u=1234 s1c=42 s1f=16 s1l=17 s2o=0 s2u=2345 s2c=53 s2f=28 s2l=29'
        )
        self.assertEqual(112233, output_state.master_uptime)
        self.assertEqual(456, output_state.master_counter, )
        self.assertEqual(7, output_state.master_backlight)

        self.assertTrue(output_state.slave1_online)
        self.assertEqual(1234, output_state.slave1_uptime)
        self.assertEqual(42, output_state.slave1_counter)
        self.assertEqual(16, output_state.slave1_fan_speed)
        self.assertEqual(17, output_state.slave1_light_intensity)

        self.assertFalse(output_state.slave2_online)
        self.assertEqual(2345, output_state.slave2_uptime)
        self.assertEqual(53, output_state.slave2_counter)
        self.assertEqual(28, output_state.slave2_fan_speed)
        self.assertEqual(29, output_state.slave2_light_intensity)
