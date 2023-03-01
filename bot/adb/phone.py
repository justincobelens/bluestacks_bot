import subprocess
import time


class Phone:
    def __post_init__(self):
        pass

    @staticmethod
    def _execute_command(*cmd, with_response=True):
        cmd = ['adb'] + [*cmd]
        result = subprocess.run(cmd, capture_output=with_response, text=True)
        if with_response:
            return result

    def start_adb_server(self):
        cmd = 'start-server'
        result = self._execute_command(cmd)
        return result.stderr

    def stop_adb_server(self):
        cmd = 'kill-server'
        result = self._execute_command(cmd)
        return result.stderr

    def connect(self, serial):
        cmd = 'connect'
        result = self._execute_command(cmd, serial)
        return result.stdout

    def disconnect(self, serial):
        cmd = 'disconnect'
        result = self._execute_command(cmd, serial)
        return result.stdout

    def disconnect_all(self):
        cmd = 'disconnect'
        result = self._execute_command(cmd)
        return result.stdout

    def devices(self):
        cmd = 'devices'
        result = self._execute_command(cmd)

        devices_raw = result.stdout.split('\n')[1::]
        devices = []

        if len(devices_raw) == 0:
            return devices

        for device in devices_raw:
            if device == '':
                continue

            device = device.split('\t')
            devices.append(device[0])

        return devices

    def is_connected(self):
        pass

    def wait_for_state(self, serial: str = None, state: str = 'device'):
        cmd = f'wait-for-{state}'

        if serial is not None:
            cmd = f'wait-for-{serial}-{state}'

        result = self._execute_command(cmd)
        return result

    def get_state(self):
        cmd = 'get-state'
        result = self._execute_command(cmd)
        return result.stdout

    # SHELL COMMANDS
    def shell(self, serial, shell_cmd):
        """
        -s [SERIAL] shell
        """
        cmd = ['-s', serial, 'shell'] + shell_cmd
        result = self._execute_command(*cmd)
        return result

    def key_event(self, serial, keyboard_value: str):
        cmd = ['input', 'keyevent', keyboard_value]
        result = self.shell(serial, cmd)
        return result

    # TODO
    # there must be a better way for creating timeouts
    def wait_for_homescreen(self, serial, cur_depth=0, max_depth=5):
        """
        adb -s [SERIAL] shell getprop sys.boot_completed | tr -d '\r'
        """

        cmd = r"getprop sys.boot_completed | tr -d '\r'"
        result = self.shell(serial, cmd.split(" "))

        timeout = 0
        try:
            stdout = result.stdout.split()[0]
        except IndexError as e:

            if cur_depth < max_depth:
                time.sleep(5)
                cur_depth += 1
                return self.wait_for_homescreen(serial)
            else:
                print(result)
                return False

        while result.stdout.split()[0] != '1':
            result = self.shell(serial, cmd.split(" "))
            time.sleep(2)

            if timeout > 10:
                print('timed out while waiting for home screen')
                return False

            timeout += 2

        self.key_event(serial, '82')

        return result

    def get_ip(self, serial):
        cmd = r"wget -q -O - ipinfo.io/ip"
        result = self.shell(serial, [cmd])
        # result = subprocess.run(["adb", '-s', serial, "shell", "wget", '-O', '-', 'ipinfo.io/ip'], capture_output=True, text=True)

        return result.stdout
