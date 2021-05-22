import time

import serial
from serial.tools import list_ports


class Core:
    MASTER_PORT_SPEED = 115200

    def __init__(self):
        super().__init__()
        self._master_port = None
        self._start_time = time.time()
        # self.state = {'slave1': {'time'}}
        self.master_work = False
        self._slave1_counter = 0
        self._slave2_counter = 1234

    @property
    def master_port(self):
        return self._master_port

    @master_port.setter
    def master_port(self, port):
        print(f'Set port: {port}')
        self.master_port = port

    @property
    def slave1_uptime(self):
        return int(time.time() - self._start_time)

    @property
    def slave1_counter(self):
        self._slave1_counter += 1
        return self._slave1_counter

    @property
    def slave2_uptime(self):
        return int(time.time() - self._start_time - 4321)

    @property
    def slave2_counter(self):
        self._slave2_counter += 1
        return self._slave1_counter



    def parse_mcu_response(self, data: str):
        print(data)

    def listen_master_port1(self):
        ser = serial.Serial(port='COM1', baudrate=self.MASTER_PORT_SPEED)

        while True:
            line = ser.readline()
            print(line)

    def thread_test(self):
        print('Started')
        i = 0
        self.master_work = True
        while self.master_work:
            i += 1
            print(i)
            time.sleep(1)
        print('Exited')
