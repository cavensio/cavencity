import configparser as configparser

from serial.tools.list_ports_common import ListPortInfo

from core import Core

core = Core()


class Model:
    INI_FILE = 'cavencity.ini'

    def __init__(self):
        super().__init__()
        self.__load_config()
        self._master_port = self.config.get('Master', 'port')

    def __load_config(self):
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(self.INI_FILE)
        self.config = config

    def __save_config(self):
        self.config.write(open(self.INI_FILE, 'w'))

    @property
    def master_port(self):
        return self._master_port

    @master_port.setter
    def master_port(self, port):
        print(f'Set master port: {port}')
        self._master_port = port
        self.config.set('Master', 'port', value=port)
        self.__save_config()

    @property
    def slave1_alias(self):
        return self.config.get('Slave1', 'alias', fallback='Slave1')

    @property
    def slave2_alias(self):
        return self.config.get('Slave2', 'alias', fallback='Slave2')

    def list_ports(self) -> list[ListPortInfo]:
        return core.list_ports()
