from abc import ABC, abstractmethod
from datetime import datetime
from os.path import join
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from rootpath import detect
from weasyprint import HTML


class Convertor(ABC):
    """ Abstract class for converting news """

    def __init__(self, logger, dir_path, file_name):
        self._logger = logger
        self.dir_path = dir_path
        self.file_name = file_name
        self.file_extension = ''

    @property
    def file(self):
        return Path(self.dir_path, self.file_name + str(datetime.now())).with_suffix('.' + self.file_extension)

    @staticmethod
    def _validate_limit(news, limit):
        """
        Validation a given limit
        :param limit: given limit
        :return: validated limit
        """
        if limit <= 0 or limit > len(news):
            return len(news)
        else:
            # self._logger.debug('Limit on the number of news: {}.'.format(limit))
            return limit

    @abstractmethod
    def convert(self, data, limit):
        """
        Abstract method for converting news
        :param data: news list
        :param limit: given limit
        """
        pass

    def write_to_file(self, news, mode):
        """
        Writing converted information to a file
        :param news: news list
        :param mode: file write type
        """
        self._logger.debug('Writing to the file "{}" has started.'.format(self.file))
        with open(self.file, mode=mode) as file:
            file.write(news)
            self._logger.debug('File writing completed.')


class ConvertorHTML(Convertor):
    """ Class for converting news into html format """

    def __init__(self, logger, dir_path, file_name='news'):
        super().__init__(logger, dir_path, file_name)
        self.file_extension = 'html'
        self.environment = Environment(loader=FileSystemLoader(self.template_dir_path))
        self.template = self.environment.get_template('template.html')

    @property
    def template_dir_path(self):
        """
        Getting the path to the file with the template
        :return: the path to the file
        """
        return join(detect(), 'rss_reader', 'data', 'template')

    def convert(self, data, limit):
        """
        Converting news into html format
        :param data: news list
        :param limit: given limit
        """
        self._logger.debug('Converting news to HTML.')
        limit = self._validate_limit(data, limit)
        news = data[:limit]
        data = self.template.render(news=news)
        if self.dir_path:
            self.write_to_file(data, 'w')
        return data


class ConvertorPDF(Convertor):
    """ Class for converting news into pdf format """

    def __init__(self, logger, dir_path, file_name='news'):
        super().__init__(logger, dir_path, file_name)
        self.file_extension = 'pdf'

    def convert(self, data, limit):
        """
        Converting news into pdf format
        :param data: news list
        :param limit: given limit
        """
        self._logger.debug('Converting news to PDF.')
        limit = self._validate_limit(data, limit)
        news = data[:limit]
        data = ConvertorHTML(logger=self._logger, dir_path=None).convert(data=news, limit=limit)
        data = HTML(string=data).write_pdf()
        self.write_to_file(data, 'wb')
        return data
