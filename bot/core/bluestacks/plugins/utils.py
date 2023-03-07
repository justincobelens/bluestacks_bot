
from bot.core.bluestacks.plugins import Plugin

from bot.utils.logger import BotLogging

logger = BotLogging.get_logger(__name__)


class Utils(Plugin):

    def arrange(self, window_title, region: list):
        # bluestacks_window = pygetwindow.getWindowsWithTitle(window_title)[0]
        window = self.get_window(window_title)

        # # set position of window
        # bluestacks_window.moveTo(region[0], region[1])
        window.moveTo(region[0], region[1])

        # # set size of window
        # bluestacks_window.resizeTo(region[2], region[3])

        raise NotImplementedError
