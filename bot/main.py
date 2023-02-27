import sys
import time

from window import Window
from bluestacks import Bluestacks
from phone import Phone

import const


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
            instance_title = instance['Name']  # e.g. BlueStacks App Player 1
            instance_name = instance['InstanceName']  # e.g. nougat64 or nougat64_2
            instance_path = f"{const.instance_path(instance_name)}"

            # 1) CREATE BLUESTACKS WINDOW
            # open window
            window.open(instance_path)

            # wait till window is open
            window.wait(instance_title)

            # arrange window
            window.arrange(instance_title, [0, 0, 593, 1020])

            # 2) CREATE ADB CONNECTION
            # get adb port
            adb_port = bluestacks.get_adb_port(instance_name)
            print(adb_port)

            sys.exit()


if __name__ == '__main__':
    main = Main()
    main.mainloop()
