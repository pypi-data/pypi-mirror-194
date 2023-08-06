import abc
import logging
import logging.config
import sys

__all__ = ['Loggable', 'get_logger_settings', 'init_logger']


class Loggable(abc.ABC):
    """Allows a class to have its own logger.

    :param logger: parent logger or None for root as parent
    """

    def __init__(self, logger: logging.Logger = None):
        self._logger = self._get_logger(logger)

    @property
    def logger(self) -> logging.Logger:
        """Instance logger."""
        return self._logger

    def _get_logger(self, logger):
        if logger:
            logger = logger.getChild(self._get_logger_name())
        else:
            logger = logging.getLogger(self._get_logger_name())
        return logger

    def _get_logger_name(self) -> str:
        name = getattr(self, 'service_name', None)
        if not name:
            name = self.__class__.__name__
        return name


class Colors:
    """Default colors."""

    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    GRAY = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


class LogFormatter(logging.Formatter):
    """Default formatter."""

    colors = {
        logging.DEBUG: Colors.GRAY,
        logging.INFO: Colors.RESET,
        logging.WARNING: Colors.YELLOW,
        logging.ERROR: Colors.YELLOW,
        logging.CRITICAL: Colors.YELLOW,
    }

    def format(self, record):
        msg = super().format(record)
        color = self.colors[record.levelno]
        return f'{color}{msg}{Colors.RESET}'


def get_logger_settings(level: str, debug: bool):
    """Get useful logger settings."""
    logger = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                '()': LogFormatter,
                'format': '%(asctime)s - %(levelname)s - %(name)s - %(message)s (%(filename)s:%(lineno)d)',
                'datefmt': '%H:%M:%S',
            }
        },
        'handlers': {
            'console': {'class': 'logging.StreamHandler', 'formatter': 'default', 'level': level, 'stream': sys.stdout},
        },
        'loggers': {'app': {'handlers': ['console'], 'level': level, 'propagate': True}},
    }
    return logger


def init_logger(settings):
    """Init logger from logger settings."""
    logger_settings = get_logger_settings(settings.main['loglevel'], settings.app.debug)
    logging.config.dictConfig(logger_settings)
    logger = logging.getLogger('app')
    return logger
