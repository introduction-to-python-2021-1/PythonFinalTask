import io
import logging
import sys
from pathlib import Path
from xhtml2pdf import pisa
from jinja2 import Template


class Converter:
    def __init__(self, directory, file_name, logger):
        self.dir = Path(directory).absolute()
        self.full_path_to_file = self.dir / file_name
        self.logger = logger
        self.template = Path(__file__).resolve().parent / "templates" / "news.html"

    def prepare_storage(self):
        try:
            self.dir.mkdir(exist_ok=True)
            self.full_path_to_file.touch(exist_ok=True)
        except PermissionError:
            logging.error("Conversion cannot be performed. Permission denied for this directory")
            sys.exit()

    def convert_to_html(self, news_list):
        self.prepare_storage()
        content = self.generate_html_template(news_list)
        self.write_to_file(content.encode("UTF-8"))

    def convert_to_pdf(self,news_list):
        self.prepare_storage()
        content = self.generate_html_template(news_list)
        pdf = io.BytesIO()
        pisa.pisaDocument(content, pdf)
        self.write_to_file(pdf.getvalue())

    def generate_html_template(self, news_list):
        with open(self.template, "r") as fp:
            template = Template(fp.read())
        return template.render(news_list=news_list)

    def write_to_file(self, content):
        try:
            with open(self.full_path_to_file, "wb") as fp:
                fp.write(content)
        except PermissionError:
            logging.error("Conversion cannot be performed. Permission denied for this directory")
            sys.exit()
