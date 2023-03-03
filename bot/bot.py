import json
from dataclasses import dataclass, field

@dataclass
class BotBase:
    manager: any
    instance_title: str
    instance_name: str
    _serial: str = "localhost:5555",
    _tasks: json = None

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
        self.manager.run()

    def stop(self):
        self.manager.stop()

    def kill(self):
        pass
