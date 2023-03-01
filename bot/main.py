import time

from bot.window.window import Window
from bot.window.bluestacks import Bluestacks
from bot.adb.phone import Phone

from bot import paths

from bot.tasks.task import Task


class Main:

    def __init__(self):
        self.window = Window()
        self.bluestacks = Bluestacks()
        self.phone = Phone()

    def mainloop(self):
        window = self.window
        bluestacks = self.bluestacks
        phone = self.phone

        instances = bluestacks.get_instances_data()
        phone.start_adb_server()

        for instance in instances:
            if len(phone.devices()) != 0:
                phone.disconnect_all()

            instance_title = instance['Name']  # e.g. BlueStacks App Player 1
            instance_name = instance['InstanceName']  # e.g. Nougat64 or Pie64_2
            instance_path = f"{paths.instance_path(instance_name)}"

            # 1) CREATE BLUESTACKS WINDOW
            # TODO
            # add check for if multiple windows are open
            # for now, only 1 window should be open at the time

            # open window
            window.open(instance_path)

            # wait for process to start
            window.wait_for_process(state='start')

            # wait till window is open
            window.wait_for_window(instance_title)

            # arrange window
            window.arrange(instance_title, [0, 0, 593, 1020])

            # 2) CONNECT ADB
            # get adb port
            adb_port = bluestacks.get_adb_port(instance_name)
            serial = f"localhost:{adb_port}"

            # connect device
            phone.connect(serial)

            # wait till device is booted
            phone.wait_for_state('local', 'device')
            phone.get_state()

            # wait for home screen to load
            phone.wait_for_homescreen(serial)

            # 3) PERFORM TASKS
            time.sleep(5)
            task = Task()
            public_ip = task.public_ip
            device_public_ip = phone.get_ip(serial)

            print(f"pc pip: {public_ip}")
            print(f"device pip: {device_public_ip}")

            # 4) DISCONNECT ADB
            phone.disconnect_all()

            # 5) CLOSE BLUESTACKS WINDOW
            window.close(instance_title)

            # wait for process to stop
            window.wait_for_process(state='stop')

        phone.stop_adb_server()


if __name__ == '__main__':
    main = Main()
    main.mainloop()
