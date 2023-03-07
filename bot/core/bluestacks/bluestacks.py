import json
import time

from bot.core.bluestacks.window import Window
from bot.core.bluestacks.emulator import Emulator
from bot.utils import paths


class Bluestacks(Window):

    def __init__(self):
        # get instance metadata from bluestacks
        self.instances_MimMetaData = self._get_instances_data()

    def emulator(self, instance_name, instance_title) -> Emulator:
        pid = self.get_pid(instance_title)
        whndl = self.get_whndl(instance_title)
        adb_port = self.get_adb_port(instance_name)

        return Emulator(self, pid, whndl, adb_port)

    def start_emulator(self, instance_name, instance_title):
        instance_path = f"{paths.instance_path(instance_name)}"

        # open window
        process = self.start_process(instance_path)

        # wait for process to start
        self.is_process(instance_title)

        # wait for window to load
        for _ in range(0, 60):
            if self.is_title(instance_title):
                break
            else:
                time.sleep(1)
        else:
            print("Failed to loading window")
            raise TimeoutError

        return process


    @staticmethod
    def _get_instances_data():
        path = paths.MimMetaData_path

        with open(path, 'r') as json_file:
            data = json.load(json_file)
            instances = data["Organization"]

            # print(json.dumps(instances, sort_keys=True, indent=4))

            return instances

    def get_adb_port(self, instance_name: str):
        return self._get_adb_port(instance_name)

    @staticmethod
    def _get_adb_port(instance_name: str):
        bluestacks_config_path = paths.bluestacks_config_path
        with open(bluestacks_config_path, 'r') as f:

            for line in f:
                if line[:3] != "bst":
                    continue

                words = line.split('.')
                if len(words) < 5:
                    continue

                if words[2] != instance_name:
                    continue

                if words[3] != 'status':
                    continue

                if words[4][:8] != 'adb_port':

                    continue

                adb_port = words[4].split('"')[1]
                return adb_port
