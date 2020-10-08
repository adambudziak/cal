import logging

from settings import app_settings

level = logging.DEBUG if app_settings.debug else logging.INFO
logging.basicConfig(level=level)


def get_logger(name):
    return logging.getLogger(name)
