import logging


def generate_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)

    return logger
