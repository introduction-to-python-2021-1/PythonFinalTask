import logging

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler('reader.log')
file_handler.setFormatter(formatter)
root_logger = logging.getLogger('logger')
root_logger.setLevel(logging.INFO)
root_logger.addHandler(file_handler)


def add_console_handler(logger_to_update):
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger_to_update.addHandler(console_handler)
    return logger_to_update
