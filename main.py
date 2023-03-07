import logging

from bot.manager import Manager
from bot.utils.logger import BotLogging

logger = BotLogging.get_logger('bot.' + __name__)
BotLogging.enable(level=logging.INFO)


class Main:

    @staticmethod
    def mainloop():
        manager = Manager()

        client = manager.AdbClient
        client.start_adb_server()

        try:
            i = 1
            while manager.queue:

                bot = manager.bot()
                bot.run()
                bot.stop()

                if i == 1:
                    break
                i += 1

        finally:
            logger.critical('Stopping adb server')
            client.kill()
            logger.debug('Server closed...')


if __name__ == '__main__':
    m = Main()
    m.mainloop()
