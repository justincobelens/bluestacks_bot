import pygetwindow
import json

from subprocess import Popen
from dataclasses import dataclass, field

import const


@dataclass
class Bluestacks:

    @staticmethod
    def get_instances_data():
        path = const.MimMetaData_path

        with open(path) as json_file:
            data = json.load(json_file)
            instances = data["Organization"]

            # print(json.dumps(instances, sort_keys=True, indent=4))

            return instances

    def get_adb_port(self, instance_name: str):

        bluestacks_config_path = const.bluestacks_config_path
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


