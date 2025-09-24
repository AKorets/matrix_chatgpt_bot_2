import logging
import os
from pathlib import Path

log_path = Path(os.path.dirname(__file__)).parent / "bot.log"


def getlogger():
    # create a custom logger if no log handler
    logger = logging.getLogger(__name__)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        # create handlers
        console_handler = logging.StreamHandler()  # Console output for Azure logs
        warn_handler = logging.StreamHandler()
        info_handler = logging.StreamHandler()
        error_handler = logging.FileHandler("bot.log", mode="a")
        console_handler.setLevel(logging.INFO)
        warn_handler.setLevel(logging.WARNING)
        error_handler.setLevel(logging.ERROR)
        info_handler.setLevel(logging.INFO)

        # create formatters
        console_format = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        warn_format = logging.Formatter(
            "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s",
        )
        error_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s",
        )
        info_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # set formatter
        console_handler.setFormatter(console_format)
        warn_handler.setFormatter(warn_format)
        error_handler.setFormatter(error_format)
        info_handler.setFormatter(info_format)

        # add handlers to logger
        #logger.addHandler(console_handler)  # Add console handler first
        logger.addHandler(warn_handler)
        logger.addHandler(error_handler)
        logger.addHandler(info_handler)

    return logger
