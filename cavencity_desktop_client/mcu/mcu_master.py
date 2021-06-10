"""
Serial interface to the master MCU.
"""
import time
from logger import log
from serial import Serial, SerialException
from serial.tools import list_ports

from mcu.mcu_master_states import MasterException, MasterSlaveTargetState, MasterSlaveActualState


class McuMaster:
    PORT_SPEED = 115200
    TIMEOUT = 1

    def __init__(self, port: str = None):
        super().__init__()
        self._port = port
        self._serial: Serial = None

    def set_state(self, input_state: MasterSlaveTargetState) -> MasterSlaveActualState:
        request = input_state.to_mcu_string().encode('ascii')
        time1 = time.time_ns()
        self._serial_write(b'S ' + request + b'\n')
        state: MasterSlaveActualState = self._read_state()
        time2 = time.time_ns()
        state.masterState.latency = (time2 - time1) // 1000
        return state

    def get_state(self) -> MasterSlaveActualState:
        self._serial_write(b'P\n')
        return self._read_state()

    def _read_state(self) -> MasterSlaveActualState:
        while True:
            line = self._serial_readline()
            if not line:
                msg = 'No response from the master'
                log.warning(msg)
                raise MasterException(msg)
            elif line[0] == 0x1e:
                return MasterSlaveActualState.from_mcu_string(line[1:].strip().decode('ascii'))

    def _check_or_open_serial(self, force_reopen=False):
        closed = True
        if self._serial and self._serial.isOpen():
            if force_reopen:
                log.info('Master close')
                self._serial.close()
            else:
                closed = False

        if closed:
            self._serial_open()
            time.sleep(1)
            self._read_welcome()

    def _read_welcome(self):
        # MCU need some time to boot
        while True:
            data = self._serial_readline()
            if not data:
                continue
            elif data == b'cavencity_dummy_master\r\n':
                log.info('Dummy master detected')
                break
            elif data == b'cavencity_master\r\n':
                log.info('Master detected')
                break
            else:
                msg = 'Unexpected master'
                log.warning(msg)
                raise MasterException(msg)

    def _serial_open(self) -> None:
        try:
            log.info(f'Opening master {self._port}')
            self._serial = Serial(port=self._port, baudrate=self.PORT_SPEED, timeout=self.TIMEOUT)
            log.info(f'Opened master {self._port}')
        except SerialException as e:
            msg = f'Can not open master {self._port}'
            log.warning(msg)
            raise MasterException(msg) from e

    def _serial_write(self, data: bytes) -> None:
        self._check_or_open_serial()
        try:
            log.info(f'Master write: {data}')
            self._serial.write(data)
        except SerialException as e:
            raise MasterException('Can write to the master') from e

    def _serial_readline(self) -> bytes:
        self._check_or_open_serial()
        try:
            data = self._serial.readline()
            log.info(f'Master read: {data}')
            return data
        except SerialException as e:
            raise MasterException('Can read from the master') from e

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        log.info(f'Set master port: {port}')
        self._port = port
        # self._check_or_open_serial(True)

    def list_ports(self):
        """
        List all COM ports in the system
        :return: ordered list of ListPortInfo objects
        """
        # return [ListPortInfo(f'COM{n}') for n in range(1, 5)]
        return sorted(list_ports.comports())
