from time import sleep

from serial import Serial
from serial.tools import list_ports

from mcu_state import OutputState, InputState


class McuControl:
    MASTER_PORT_SPEED = 115200

    def __init__(self):
        super().__init__()
        self._master_port = None
        self._master_serial: Serial = None

    def push_state(self, input_state_string: InputState) -> OutputState:
        self.__check_or_open_master_port(True)

        input_state_string.to_mcu_string()
        # ser.write(f'V{i} X{randint(10, 99)}R'.encode('ascii'))
        self._master_serial.write(b'P')

        # if line[0] == 30:
        #     print(decode_response(line[1:].strip().decode('ascii')))
        # else:
        #     line = line.strip().decode('ascii')
        #     print(f'MCU message: {line}')
        sleep(0.25)
        return self.read_state()

    def read_state(self) -> OutputState:
        self._master_serial.write(b'R')
        line = self._master_serial.readline()
        if line[0] == 0x1e:
            print(f'Response: {line}')
            return OutputState.from_mcu_string(line[1:].strip().decode('ascii'))
        else:
            line = line.strip().decode('ascii')
            print(f'MCU message: {line}')
            # todo throw exception

    def __check_or_open_master_port(self, force_reopen=False):
        closed = True
        if self._master_serial and self._master_serial.isOpen():
            if force_reopen:
                self._master_serial.close()
            else:
                closed = False

        if closed:
            self._master_serial = Serial(port=self._master_port, baudrate=self.MASTER_PORT_SPEED)
            # Read welcome line
            welcome_line = self._master_serial.readline()
            if welcome_line == b'mcu_serial\r\n':
                print('mcu_serial detected')
            else:
                pass  # todo throw exception

    @property
    def master_port(self):
        return self._master_port

    @master_port.setter
    def master_port(self, port):
        print(f'Set port: {port}')
        self._master_port = port
        self.__check_or_open_master_port(True)

    def list_ports(self):
        """
        List all COM ports in the system
        :return: ordered list of ListPortInfo objects
        """
        # return [ListPortInfo(f'COM{n}') for n in range(1, 5)]
        return sorted(list_ports.comports())
