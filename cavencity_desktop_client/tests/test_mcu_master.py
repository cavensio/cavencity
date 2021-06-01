import unittest

from mcu_master import McuMaster
from mcu_master_states import MasterException

MASTER_PORT = 'COM3'


@unittest.skipUnless(MASTER_PORT, '''
This test works with a real hardware.
Point MASTER_PORT to the MCU where "cavencity_dummy_master" program is uploaded.
''')
class TestMcuMaster(unittest.TestCase):

    def test_read_state_fail(self):
        mcu = McuMaster('NOT_A_PORT')
        with self.assertRaises(MasterException):
            mcu.get_state()

    def test_read_state(self):
        mcu = McuMaster(MASTER_PORT)
        state = mcu.get_state()
        self.assertGreater(state.master_uptime, 0)
        self.assertGreater(state.master_counter, 0)
        self.assertGreater(state.slave1_uptime, 0)
        self.assertGreater(state.slave1_counter, 0)
        self.assertGreater(state.slave2_uptime, 0)
        self.assertGreater(state.slave2_counter, 0)

    def test_timeout(self):
        mcu = McuMaster(MASTER_PORT)
        mcu._serial_write(b'T1500')
        with self.assertRaises(MasterException):
            mcu.get_state()
