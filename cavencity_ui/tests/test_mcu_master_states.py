import unittest

from mcu_master_states import MasterInputState, MasterOutputState


class TestMasterInputState(unittest.TestCase):
    def test_to_mcu_string(self):
        input_state = MasterInputState(5, 3, 4, 1, 2)
        self.assertEquals(input_state.to_mcu_string(), 'mb=5 s1f=3 s1l=4 s2f=1 s2l=2')


class TestMasterOutputState(unittest.TestCase):
    def test_from_mcu_string(self):
        output_state = MasterOutputState.from_mcu_string(
            'mu=112233 mc=456 mb=7 s1o=1 s1u=1234 s1c=42 s1f=16 s1l=17 s2o=0 s2u=2345 s2c=53 s2f=28 s2l=29'
        )
        self.assertEqual(output_state.master_uptime, 112233)
        self.assertEqual(output_state.master_counter, 456)
        self.assertEqual(output_state.master_backlight, 7)

        self.assertTrue(output_state.slave1_online)
        self.assertEqual(output_state.slave1_uptime, 1234)
        self.assertEqual(output_state.slave1_counter, 42)
        self.assertEqual(output_state.slave1_fan_speed, 16)
        self.assertEqual(output_state.slave1_light_intensity, 17)

        self.assertFalse(output_state.slave2_online)
        self.assertEqual(output_state.slave2_uptime, 2345)
        self.assertEqual(output_state.slave2_counter, 53)
        self.assertEqual(output_state.slave2_fan_speed, 28)
        self.assertEqual(output_state.slave2_light_intensity, 29)
