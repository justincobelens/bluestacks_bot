from bot.adb.device import Device
from bot.adb.command import Command


class Host(Command):

    def _execute_cmd(self, cmd, with_response=True):
        with self.create_connection() as conn:
            conn.send(cmd)
            if with_response:
                result = conn.receive()
                return result
            else:
                conn.check_status()

    def devices(self):
        cmd = "host:devices"
        result = self._execute_cmd(cmd)

        devices = []

        for line in result.split('\n'):
            if not line:
                break

            tokens = line.split()

            devices.append(Device(self, tokens[0]))

        return devices

    def kill(self):
        """
            Ask the ADB server to quit immediately. This is used when the
            ADB client detects that an obsolete server is running after an
            upgrade.
        """
        with self.create_connection() as conn:
            conn.send("host:kill")

        return True

    def remote_connect(self, host, port):
        cmd = "host:connect:%s:%d" % (host, port)
        result = self._execute_cmd(cmd)

        return "connected" in result

    def remote_disconnect(self, host=None, port=None):
        cmd = "host:disconnect:"
        if host:
            cmd = "host:disconnect:{}".format(host)
            if port:
                cmd = "{}:{}".format(cmd, port)

        return self._execute_cmd(cmd)
