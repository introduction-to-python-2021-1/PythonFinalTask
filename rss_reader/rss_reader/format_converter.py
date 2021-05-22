import io
import abc
import sys
from pathlib import Path

import jinja2
from xhtml2pdf import pisa

try:
    from helper import get_path_to_data
    from logger_config import get_logger
except ImportError:
    from .helper import get_path_to_data
    from .logger_config import get_logger


class Converter(abc.ABC):
    """Creates abstract converter from which concrete converters must be derived."""

    @staticmethod
    def generate_html(news_items):
        """
        Generates HTML with news items.

        Parameters:
            news_items [{"Feed": (str), "Title", (str), "Date": (srt), "Link": (str), "image_url": (str)}]: [] of {}'s

        Returns:
            (str): String containing HTML with news items.
        """
        htmlpath = get_path_to_data("html")
        template_loader = jinja2.FileSystemLoader(searchpath=htmlpath)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template("template.html")

        return template.render(news_items=news_items)

    def __init__(self, *, directory_path, file_name):
        self.file_path = Path(directory_path).absolute() / file_name

    def create_file(self, content):
        """
        Creates file with content. Format of content depends on class which instance calls this method.

        Parameters:
            content (bytes): Bytes object with content to write to file.
        """
        self.file_path.touch(exist_ok=True)
        self.file_path.write_bytes(content)

    @abc.abstractmethod
    def convert(self, news_items):
        """
        Converts news items to corresponding format of class that implements this method.

        Parameters:
            news_items [{"Feed": (str), "Title", (str), "Date": (srt), "Link": (str), "image_url": (str)}]: [] of {}'s
        """
        pass


class ToHtmlConverter(Converter):
    """Implements converter to HTML and interface to interact with it."""

    def convert(self, news_items):
        """
        Converts news items to HTML format.

        Parameters:
            news_items [{"Feed": (str), "Title", (str), "Date": (srt), "Link": (str), "image_url": (str)}]: [] of {}'s
        """
        html_content = self.generate_html(news_items)
        self.create_file(html_content.encode("UTF-8"))


class ToPdfConverter(Converter):
    """Implements converter to PDF and interface to interact with it."""

    def convert(self, news_items):
        """
        Converts news items to PDF format.

        Parameters:
            news_items [{"Feed": (str), "Title", (str), "Date": (srt), "Link": (str), "image_url": (str)}]: [] of {}'s
        """
        html_content = self.generate_html(news_items)
        pdf_content = io.BytesIO()
        pisa.pisaDocument(html_content.encode("UTF-8"), pdf_content, encoding="UTF-8", path=get_path_to_data("fonts"))
        self.create_file(pdf_content.getvalue())
