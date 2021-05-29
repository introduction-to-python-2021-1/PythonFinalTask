import logging

_log_file_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) \n %(message)s"
_log_stream_format = f"[%(levelname)s] - (%(filename)s).%(funcName)s(%(lineno)d) \n %(message)s"

file_handler = logging.FileHandler("rss_reader.log", "w")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(_log_file_format))

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)
stream_handler.setFormatter(logging.Formatter(_log_file_format))

# def get_file_handler():
#     file_handler = logging.FileHandler("rss_reader.log", "w")
#     file_handler.setLevel(logging.INFO)
#     file_handler.setFormatter(logging.Formatter(_log_file_format))
#     return file_handler
#
# def get_stream_handler():
#     stream_handler = logging.StreamHandler()
#     stream_handler.setLevel(logging.ERROR)
#     stream_handler.setFormatter(logging.Formatter(_log_file_format))
#     return stream_handler

def get_logger(name):
    global file_handler
    global stream_handler
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
