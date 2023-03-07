from bot.bluestacks.plugins.utils import Utils


class Emulator(Utils):

    def __init__(self, bluestacks, pid, whndl, adb_port):
        self.bluestacks = bluestacks
        self.pid = pid
        self.whndl = whndl
        self.adb_port = adb_port

    def create_connection(self, set_transport=True, timeout=None):
        conn = self.bluestacks.create_connection(timeout=timeout)
