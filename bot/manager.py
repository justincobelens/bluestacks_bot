import collections
import time

from bot.bsbot import Bot
from bot.core.adb import Client
from bot.core.bluestacks.bluestacks import Bluestacks
from bot.utils.logger import BotLogging

logger = BotLogging.get_logger("bot." + __name__)


class Manager:

    def __init__(self):
        # initiate objects
        self.bluestacks = Bluestacks()
        self.AdbClient = Client()

        # creating all bots and put in queue
        self.bots_list = list(map(self.__create_bot, self.bluestacks.instances_MimMetaData))
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

    def run(self, bot):
        self.__start_emulator(bot)
        self.__start_device(bot)

    def stop(self, bot):
        self.__stop_device(bot)
        self.__stop_emulator(bot)

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

    def __start_emulator(self, bot):

        # start emulator window
        self.bluestacks.start_emulator(bot.instance_name, bot.instance_title)

        # create emulator obj
        emulator = self.bluestacks.emulator(bot.instance_name, bot.instance_title)

        # update bot adb_port
        bot.adb_port = emulator.adb_port

        # arrange window
        emulator.arrange(self, [0, 0, 593, 1020])

    def __start_device(self, bot):
        #  bot = self.active_bot[0]

        serial = f"localhost:{bot.adb_port}"
        bot.serial = serial  # update bot serial

        # connect to device
        self.AdbClient.remote_connect(host="localhost", port=int(bot.adb_port))

        # create phone
        self.phone = self.AdbClient.device(serial)
        self.phone.wait_boot_complete()

        # wait for home screen to load
        for _ in range(0, 60):
            if self.phone.get_top_activity() == 'com.bluestacks.launcher/.activity.HomeActivity':
                return True
            else:
                time.sleep(1)
        else:
            print("Failed to load homescreen")
            raise TimeoutError

        #
        # self.phone.wait_for_homescreen()

    def __stop_emulator(self, bot):
        # close bluestacks window
        self.bluestacks.close(bot.instance_title)

        # wait for process to stop
        for _ in range(0, 60):
            if self.bluestacks.is_process(bot.instance_title):
                time.sleep(1)
                continue
            else:
                break
        else:
            print("Failed to stop emulator")
            raise TimeoutError

    def __stop_device(self, bot):
        # disconnect device from adb server
        self.AdbClient.remote_disconnect()
