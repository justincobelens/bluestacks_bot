import json
from dataclasses import dataclass, field

from bot.utils.logger import BotLogging


logger = BotLogging.get_logger("bot." + __name__)



@dataclass
class BotBase:
    manager: any
    instance_title: str
    instance_name: str
    _adb_port: str = "5555"
    _serial: str = "localhost:5555",
    _tasks: json = None

    @property
    def adb_port(self):
        return self._adb_port

    @adb_port.setter
    def adb_port(self, val):
        self._adb_port = val

    @property
    def serial(self):
        return self._serial

    @serial.setter
    def serial(self, val):
        self._serial = val

    @property
    def tasks(self):
        return self._tasks

    @tasks.setter
    def tasks(self, val):
        self._tasks = val


@dataclass
class Bot(BotBase):
    def __post_init__(self):
        pass

    def run(self):
        logger.info(f'Starting {self.instance_title}')
        self.manager.run(self)

    def stop(self):
        logger.info(f'Stopping {self.instance_title}')
        self.manager.stop(self)

    def kill(self):
        raise NotImplementedError

    def start_task(self):
        raise NotImplementedError

    def stop_task(self):
        raise NotImplementedError
