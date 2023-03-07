from bot.core.adb.command.shell import Shell
from bot.core.adb.plugins.utils import Utils

class Device(Shell, Utils):

    def __init__(self, client, serial):
        self.client = client
        self.serial = serial

    def create_connection(self, set_transport=True, timeout=None):
        conn = self.client.create_connection(timeout=timeout)

        if set_transport:
            self.transport(conn)

        return conn
