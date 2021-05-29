"""
This module provides tools for logging while program is working
"""


import logging


def create_root_logger():
    """
    Creates root logger
    """
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler('reader.log')
    file_handler.setFormatter(formatter)
    root_logger = logging.getLogger('logger')
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    return root_logger


def add_console_handler(logger_to_update):
    """
    Add console handler to existing logger
    """
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger_to_update.addHandler(console_handler)
    return logger_to_update
