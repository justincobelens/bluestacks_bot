import collections
from dataclasses import replace

from bot import paths
from bot import Bot
from bot.adb.client import Client
from bot.window.bluestacks import Bluestacks
from bot.window.window import Window


class Manager:

    def __init__(self):
        # initiate objects
        self.bluestacks = Bluestacks()
        self.window = Window()
        self.AdbClient = Client()

        # get instance metadata from bluestacks
        self.instances_MimMetaData = self.bluestacks.get_instances_data()

        # creating all bots and put in queue
        self.bots_list = list(map(self.__create_bot, self.instances_MimMetaData))
        self.queue = collections.deque(self.bots_list)

        #
        self.active_bot = []

        #############################################
        #           Public Methods                  #
        #############################################

    def bot(self) -> Bot:
        if len(self.active_bot) == 0:
            self.active_bot.append(self.queue.popleft())
        else:
            self.active_bot[0] = self.queue.popleft()

        return self.active_bot[0]

    def run(self):
        self.__start_bluestacks()
        self.__start_phone()

    def stop(self):
        self.__stop_phone()
        self.__stop_bluestacks()

        #############################################
        #           Private Methods                 #
        #############################################

    def __create_bot(self, instance) -> Bot:
        instance_title = instance['Name']  # e.g. BlueStacks App Player 1
        instance_name = instance['InstanceName']  # e.g. Nougat64 or Pie64_2

        bot = Bot(self,
                  instance_title,
                  instance_name)
        return bot

    def __start_bluestacks(self):
        bot = self.active_bot[0]
        self.window = Window()

        # open window
        instance_path = f"{paths.instance_path(bot.instance_name)}"
        self.window.open(instance_path)

        # wait for process to start
        self.window.wait_for_process(state='start')

        # wait till window is open
        self.window.wait_for_window(bot.instance_title)

        # arrange window
        self.window.arrange(bot.instance_title, [0, 0, 593, 1020])

    def __start_phone(self):
        bot = self.active_bot[0]

        adb_port = self.bluestacks.get_adb_port(bot.instance_name)
        serial = f"localhost:{adb_port}"
        bot.serial = serial

        # connect device
        self.AdbClient.remote_connect(host="localhost", port=int(adb_port))
        self.phone = self.AdbClient.device(serial)
        self.phone.wait_boot_complete()

        # # wait for home screen to load
        # self.phone.wait_for_homescreen()

    def __stop_bluestacks(self):
        bot = self.active_bot[0]

        # close bluestacks window
        self.window.close(bot.instance_title)

        # wait for process to stop
        self.window.wait_for_process(state='stop')

    def __stop_phone(self):
        # disconnect device from adb server
        self.AdbClient.remote_disconnect()

