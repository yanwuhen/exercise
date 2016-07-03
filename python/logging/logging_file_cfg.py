import logging
from logging.config import fileConfig

fileConfig('logging.cfg')
logger = logging.getLogger()
logger.debug('often makes a very good meal of %s', 'visiting tourists')
