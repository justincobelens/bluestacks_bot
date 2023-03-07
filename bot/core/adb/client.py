import subprocess

from bot.core.adb.connection import Connection
from bot.core.adb.command.host import Host


class Client(Host):
    def __init__(self, host='127.0.0.1', port=5037):
        self.host = host
        self.port = port

    @staticmethod
    def start_adb_server():
        result = subprocess.run(['adb', 'start-server'], capture_output=True, text=True)
        return result

    def create_connection(self, timeout=None):
        conn = Connection(self.host, self.port, timeout)
        conn.connect()
        return conn

    def device(self, serial):
        devices = self.devices()

        for device in devices:
            if device.serial == serial:
                return device

        return None
