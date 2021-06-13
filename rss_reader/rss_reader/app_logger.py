import logging
import os

# set logger format for file logs and stdout
_log_file_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) \n %(message)s"
_log_stream_format = f"[%(levelname)s] -- %(message)s"

# creating a file handler
# assigning a level and formatter to it

tmp_folder_path = "tmp" + os.path.sep
if not os.path.exists(tmp_folder_path):
    os.makedirs(tmp_folder_path)
logs_path = tmp_folder_path + "rss_reader.log"

file_handler = logging.FileHandler(logs_path, "w")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(_log_file_format))

# creating a stream handler
# assigning a level and formatter to it
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)
stream_handler.setFormatter(logging.Formatter(_log_stream_format))

# The function returns a reference to the logger object.
# Thus, there will be one logger for the entire module.
# And, since we create only one object for the file and stream handlers
# they will also be the same for the entire module.


def get_logger(name):
    global file_handler
    global stream_handler
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
