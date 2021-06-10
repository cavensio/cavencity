import unittest

from mcu.mcu_master import McuMaster
from mcu.mcu_master_states import MasterException

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
        self.assertEqual(state.masterState.uptime, 0)
        self.assertGreater(state.masterState.counter, 0)
        self.assertGreater(state.slaveStates[0].uptime, 0)
        self.assertGreater(state.slaveStates[0].counter, 0)
        self.assertEqual(state.slaveStates[1].uptime, 0)
        self.assertEqual(state.slaveStates[1].counter, 0)

    def test_timeout(self):
        mcu = McuMaster(MASTER_PORT)
        mcu._serial_write(b'T1500')
        with self.assertRaises(MasterException):
            mcu.get_state()
