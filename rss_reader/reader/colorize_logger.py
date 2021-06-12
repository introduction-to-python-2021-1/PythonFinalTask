import logging.handlers
import sys
from colored import fg, attr


class ColorizeLogger:
    """Creates a logger item with the necessary attributes"""
    def __init__(self, disable=50, is_colorize=False):
        """Logger init"""
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
        logger = logging.getLogger("")
        logger.setLevel(logging.INFO)
        handler = logging.handlers.RotatingFileHandler('../../../logs.txt')
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logging.disable(disable)
        self.is_colorize = is_colorize
        self.logger = logger
        self.debug_color = '1'
        self.info_color = '2'
        self.warning_color = '3'
        self.error_color = '4'
        self.print_color = '5'

    def debug(self, value):
        """Debug log"""
        self.logger.debug(self.get_message(self.debug_color, value))

    def info(self, value):
        """Debug info"""
        self.logger.info(self.get_message(self.info_color, value))

    def warning(self, value):
        """Debug warning"""
        self.logger.warning(self.get_message(self.warning_color, value))

    def error(self, value):
        """Debug error"""
        self.logger.error(self.get_message(self.error_color, value))

    def print(self, value):
        """Debug print"""
        print(self.get_message(self.print_color, value))

    def get_message(self, color, value):
        """Initializes the color display of the value"""
        if self.is_colorize:
            return '%s %s %s' % (fg(color), value, attr(0))
        else:
            return value
