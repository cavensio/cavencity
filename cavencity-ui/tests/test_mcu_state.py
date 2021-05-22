import unittest

from mcu_state import InputState, OutputState


class TestInputState(unittest.TestCase):
    def test_to_mcu_string(self):
        input_state = InputState(5, 3, 4, 1, 2)
        self.assertEquals(input_state.to_mcu_string(), 'mli=5,s1fs=3,s1li=4,s2fs=1,s2li=2')


class TestOutputState(unittest.TestCase):
    def test_from_mcu_string(self):
        output_state = OutputState()
        output_state.from_mcu_string(
            'mu=112233,mc=456,mli=7,s1o=1,s1u=1234,s1c=42,s1fs=16,s1li=17,s2o=0,s2u=2345,s2c=53,s2fs=28,s2li=29'
        )
        self.assertEqual(output_state.master_uptime, 112233)
        self.assertEqual(output_state.master_counter, 456)
        self.assertEqual(output_state.master_light_intensity, 7)

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
