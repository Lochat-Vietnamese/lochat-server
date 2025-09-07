import logging

class LogHelper:

    @staticmethod
    def info(message: str):
        logging.getLogger(__name__).info(message)

    @staticmethod
    def warning(message: str):
        logging.getLogger(__name__).warning(message)

    @staticmethod
    def error(message: str, exc_info: bool = False):
        logging.getLogger(__name__).error(message, exc_info=exc_info)

    @staticmethod
    def debug(message: str):
        logging.getLogger(__name__).debug(message)
