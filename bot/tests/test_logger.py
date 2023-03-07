import logging

from bot.utils.logger import BotLogging

logger = BotLogging.get_logger('bot.' + __name__)
logger.addHandler(logging.StreamHandler())
logger = BotLogging.get_logger('bot.' + __name__)

# BotLogging.enable(level=logging.DEBUG)

logger.debug('debug')

logger.info('info')
logger.warning('warning')
logger.error('error')
logger.critical('critical')