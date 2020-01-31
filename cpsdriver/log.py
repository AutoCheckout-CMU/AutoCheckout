import logging
import sys

ROOT_LOGGER = logging.getLogger()

LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}


def setup_logger(level):
    level = level.lower()
    ROOT_LOGGER.setLevel(LOG_LEVELS.get(level, logging.NOTSET))
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    ROOT_LOGGER.addHandler(handler)
