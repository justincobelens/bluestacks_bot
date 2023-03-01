from dataclasses import dataclass, field


@dataclass
class Bot:
    instance_title: str  # e.g. BlueStacks App Player 1
    instance_name: str  # e.g. Nougat64 or Pie64_2
    instance_path: str

    serial: str = field(init=False)
    adb_port: str = field(init=False)

    def __post_init__(self):
        pass

    def start(self):
        pass

    def exit(self):
        pass

    def kill(self):
        pass
