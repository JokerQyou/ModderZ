# coding: utf-8
import logging


def get_logger(name, level=logging.WARN):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    shandler = logging.StreamHandler()
    shandler.setLevel(level)

    logger.addHandler(shandler)
    return logger