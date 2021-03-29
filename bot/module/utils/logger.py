import time
import os

import logging
def get_logger(level):
    date = time.strftime("%Y-%m-%d", time.localtime())
    logger = logging.getLogger()
    logger.setLevel('DEBUG')
    BASIC_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel('DEBUG')
    log_file_full = logging.FileHandler('logs/logging_error.log')
    log_file_level = logging.FileHandler('logs/logging_error.log')
    if level == "info":
        log_file_full = logging.FileHandler('logs/full/' + date + '.log')
        log_file_level = logging.FileHandler('logs/info/' + date + '-info.log')
    if level == "warning":
        log_file_full = logging.FileHandler('logs/full/' + date + '.log')
        log_file_level = logging.FileHandler('logs/warning/' + date + '-warning.log')
    if level == "error":
        log_file_full = logging.FileHandler('logs/full/' + date + '.log')
        log_file_level = logging.FileHandler('logs/error/' + date + '-error.log')
    log_file_full.setFormatter(formatter)
    log_file_level.setFormatter(formatter)
    logger.addHandler(console)
    logger.addHandler(log_file_full)
    logger.addHandler(log_file_level)
    return logger


def info(message):
    logger = get_logger("info")
    logger.info(message)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)


def warning(message):
    logger = get_logger("warning")
    logger.warning(message)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)


def error(message):
    logger = get_logger("error")
    logger.error(message)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)


def logger_start_check():
    try:
        path = "logs"
        if not os.path.exists(path):
            os.makedirs(path)
        path = "logs/full"
        if not os.path.exists(path):
            os.makedirs(path)
        path = "logs/info"
        if not os.path.exists(path):
            os.makedirs(path)
        path = "logs/warning"
        if not os.path.exists(path):
            os.makedirs(path)
        path = "logs/error"
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        error(e.args)
