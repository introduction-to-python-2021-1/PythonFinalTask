import io
import abc
import sys
from pathlib import Path

import jinja2
from xhtml2pdf import pisa


class Converter(abc.ABC):

    @staticmethod
    def generate_html(news_items):
        template_loader = jinja2.FileSystemLoader(searchpath="data/html")
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template("template.html")

        return template.render(news_items=news_items)

    def __init__(self, *, directory_path, file_name):
        self.file_path = Path(directory_path).absolute() / file_name

    def create_file(self, content):
        self.file_path.touch(exist_ok=True)
        self.file_path.write_bytes(content)

    @abc.abstractmethod
    def convert(self, news_items):
        pass


class ToHtmlConverter(Converter):

    def convert(self, news_items):
        html_content = self.generate_html(news_items)
        self.create_file(html_content.encode("UTF-8"))


class ToPdfConverter(Converter):

    def convert(self, news_items):
        html_content = self.generate_html(news_items)
        pdf_content = io.BytesIO()
        pisa.pisaDocument(html_content.encode("UTF-8"), pdf_content, encoding="UTF-8", path="data/fonts")
        self.create_file(pdf_content.getvalue())
