import logging

BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"


class ColorFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        if record.levelno == logging.INFO:
            return f"{BLUE}{message}{RESET}"
        if record.levelno >= logging.ERROR:
            return f"{RED}{message}{RESET}"
        return message


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        formatter = ColorFormatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        file_handler = logging.FileHandler("logging.log")
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    return logger
