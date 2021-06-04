import logging.handlers
import sys
import configparser


class ColorizeLogger:
    """Creates a logger item with the necessary attributes"""
    debug_color = '37'
    info_color = '32'
    warning_color = '35'
    error_color = '91'
    print_color = '33'

    def __init__(self, disable=50, is_colorize=False, path='logger.ini'):
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
        self.set_properties(path)

    def set_properties(self, path):
        """Sets colors from file"""
        config = configparser.ConfigParser()
        try:
            config.read(path)
            self.debug_color = config['levels']['debug']
            self.info_color = config['levels']['info']
            self.warning_color = config['levels']['warning']
            self.error_color = config['levels']['error']
            self.print_color = config['methods']['print']
        except Exception:
            pass

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
            return f'\33[{color}m{value}'
        else:
            return value
