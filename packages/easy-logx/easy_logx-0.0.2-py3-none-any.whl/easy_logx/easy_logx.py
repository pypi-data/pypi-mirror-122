from typing import Any, Union
import logging

LOGGER_LEVEL = Union[logging.DEBUG, logging.INFO, logging.ERROR]
MODE = Union['w', 'a']

def test():
    print('test')

class EasyLogx:
    def __init__(self, logger_name: str = __name__, log_level: LOGGER_LEVEL = logging.DEBUG) -> None:
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)
        self.log_level = log_level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        self.logger.add(console_handler)

    def add_filehandler(self, filename: str = 'default.log', mode: MODE = 'w'):
        file_handler = logging.FileHandler(filename, mode)
        file_handler.setLevel(self.log_level)
        self.logger.add(file_handler)
