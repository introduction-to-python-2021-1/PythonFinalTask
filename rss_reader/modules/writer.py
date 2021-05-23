import os
from abc import ABC, abstractmethod
from json import dump


class Writer(ABC):
    _file_expansion = ''

    def __init__(self, logger, path=os.getcwd(), name='result'):
        self.logger = logger
        self._file_path = path
        self._file_name = name

    @property
    def file(self):
        """
        Creating a complete file path
        :return: the path to the file
        """
        path_with_name = os.path.join(self._file_path, self._file_name)
        return '.'.join([path_with_name, self._file_expansion])

    @abstractmethod
    def write(self, data):
        """
        Writing information to a file
        :param data: data for recording
        """
        pass

    def __str__(self):
        return self.file


class WriterJSON(Writer):
    _file_expansion = 'json'

    def write(self, data):
        self.logger.debug('Recording news in JSON file')
        try:
            with open(self.file, 'w', encoding='utf-8') as file:
                dump(data, file, ensure_ascii=False, indent=3)
                self.logger.debug('News recorded successfully.')
        except EnvironmentError:
            self.logger.error('Error writing to file')
