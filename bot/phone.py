import subprocess


class Phone:
    def __post_init__(self):
        pass

    @staticmethod
    def _execute_command(cmd, with_response=True):
        result = subprocess.run(['adb', f"{cmd}"], capture_output=with_response, text=True)
        if with_response:
            return result

    def start_adb_server(self):
        cmd = 'start-server'
        result = self._execute_command(cmd)

    def stop_adb_server(self):
        cmd = 'kill-server'
        result = self._execute_command(cmd)
