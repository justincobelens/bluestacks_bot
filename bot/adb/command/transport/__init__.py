import re
import time

from bot.adb.command import Command


class Transport(Command):

    def transport(self, connection):
        cmd = "host:transport:{}".format(self.serial)
        connection.send(cmd)

        return connection

    def shell(self, cmd, handler=None, timeout=None):
        conn = self.create_connection(timeout=timeout)

        cmd = "shell:{}".format(cmd)
        conn.send(cmd)

        if handler:
            handler(conn)
        else:
            result = conn.read_all()
            conn.close()
            return result.decode('utf-8')

    def list_features(self):
        result = self.shell("pm list features 2>/dev/null")

        result_pattern = "^feature:(.*?)(?:=(.*?))?\r?$"
        features = {}
        for line in result.split('\n'):
            m = re.match(result_pattern, line)
            if m:
                value = True if m.group(2) is None else m.group(2)
                features[m.group(1)] = value

        return features

    def list_packages(self):
        result = self.shell("pm list packages 2>/dev/null")
        result_pattern = "^package:(.*?)\r?$"

        packages = []
        for line in result.split('\n'):
            m = re.match(result_pattern, line)
            if m:
                packages.append(m.group(1))

        return packages

    def get_properties(self):
        result = self.shell("getprop")
        result_pattern = "^\[([\s\S]*?)\]: \[([\s\S]*?)\]\r?$"

        properties = {}
        for line in result.split('\n'):
            m = re.match(result_pattern, line)
            if m:
                properties[m.group(1)] = m.group(2)

        return properties

    def reboot(self):
        conn = self.create_connection()

        with conn:
            conn.send("reboot:")
            conn.read_all()

        return True

    def root(self):
        # Restarting adbd as root
        conn = self.create_connection()
        with conn:
            conn.send("root:")
            result = conn.read_all().decode('utf-8')

            if "restarting adbd as root" in result:
                return True
            else:
                raise RuntimeError(result.strip())

    def wait_boot_complete(self, timeout=60, timedelta=1):
        """
        :param timeout: second
        :param timedelta: second
        """
        cmd = 'getprop sys.boot_completed'

        end_time = time.time() + timeout

        while True:
            try:
                result = self.shell(cmd)
            except RuntimeError as e:
                continue

            if result.strip() == "1":
                return True

            if time.time() > end_time:
                raise TimeoutError()
            elif timedelta > 0:
                time.sleep(timedelta)
