import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='runtime.log', encoding='utf-8', level=logging.DEBUG)
logger.debug('Logger created')
