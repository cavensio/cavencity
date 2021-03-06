import configparser as configparser

from logger import log
from serial.tools.list_ports_common import ListPortInfo

from mcu.mcu_master import McuMaster
from mcu.mcu_master_states import MasterSlaveTargetState, MasterSlaveActualState, MasterException


class Model:
    INI_FILE = 'cavencity.ini'

    def __init__(self):
        super().__init__()
        self.__load_config()
        self.target_state = MasterSlaveTargetState()
        self.actual_state = MasterSlaveActualState()
        self._master = McuMaster()

    def load(self):
        self._master.port = self.config.get('Master', 'port')

    def __load_config(self):
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(self.INI_FILE)
        self.config = config

    def __save_config(self):
        self.config.write(open(self.INI_FILE, 'w'))

    @property
    def master_port(self):
        return self._master.port

    @master_port.setter
    def master_port(self, port):
        log.info(f'Set master port: {port}')
        self._master.port = port
        self.config.set('Master', 'port', value=port)
        self.__save_config()

    @property
    def slave1_alias(self):
        return self.config.get('Slave1', 'alias', fallback='Slave1')

    @property
    def slave2_alias(self):
        return self.config.get('Slave2', 'alias', fallback='Slave2')

    def list_ports(self) -> list[ListPortInfo]:
        return self._master.list_ports()

    def tick(self):
        log.info('tick')
        try:
            self.actual_state = self._master.set_state(self.target_state)
        except MasterException as e:
            self.actual_state = MasterSlaveActualState()
