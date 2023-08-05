"""L O G G E R"""
import os
from pathlib import Path
import logging

log_format = (
    "%(asctime)s [%(levelname)s] - %(name)s - %(funcName)15s:%(lineno)d - %(message)s"
)
try:
    file_handler = logging.FileHandler("data/application.log")
except FileNotFoundError:
    curr = os.getcwd()
    file_handler = Path('curr/data/application.log').touch()
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(log_format))

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
stream_handler.setFormatter(logging.Formatter(log_format))


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger
