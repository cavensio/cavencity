import unittest

from mcu_control import McuControl


class TestMcuControl(unittest.TestCase):

    # @unittest.skip('it works with real hardware')
    def test_read_state(self):
        mcu = McuControl()
        mcu.master_port = 'COM3'
        state = mcu.read_state()
        self.assertIsNotNone(state)
