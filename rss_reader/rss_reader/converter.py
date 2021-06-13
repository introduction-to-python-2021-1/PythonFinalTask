import hashlib
import io
import logging
import os
import sys
from pathlib import Path

from jinja2 import Template
from xhtml2pdf import pisa

ROOT_DIR = Path(__file__).resolve().parent.parent


class Converter:
    """This class is implementation of converter to PDF and HTML format"""

    def __init__(self, directory, file_name, logger, cache_path):
        """This initialization method receives directory from user, which will be used for saving file,
        also receives file_name and logger"""
        image_storage = ROOT_DIR / cache_path / "images"
        image_storage.mkdir(exist_ok=True)
        self.img_storage = image_storage
        self.dir = Path(directory).absolute()
        self.full_path_to_file = self.dir / file_name
        self.logger = logger
        self.template = Path(__file__).resolve().parent / "templates" / "news.html"

    def prepare_storage(self):
        """This method creates storage if it exists"""
        self.logger.info("Preparing storage for your data...")
        try:
            self.dir.mkdir(exist_ok=True)
            self.full_path_to_file.touch(exist_ok=True)
        except PermissionError:
            logging.error(
                "Conversion cannot be performed. Permission denied for this directory"
            )
            sys.exit()

    def convert_to_html(self, news_list):
        """This method converts news in HTML format and save file to directory"""
        self.logger.info("Converting news to HTML...")
        self.prepare_storage()
        self.process_news_list_with_images(news_list)
        content = self.generate_html_template(news_list)
        self.write_to_file(content.encode("UTF-8"))

    def convert_to_pdf(self, news_list):
        """This method converts news in PDF format and save it to directory"""
        self.logger.info("Converting news to PDF...")
        self.prepare_storage()
        self.process_news_list_with_images(news_list)
        content = self.generate_html_template(news_list)
        pdf = io.BytesIO()
        pisa.pisaDocument(content, pdf)
        self.write_to_file(pdf.getvalue())

    def generate_html_template(self, news_list):
        """This method generate HTML template and render it"""
        with open(self.template, "r") as fp:
            template = Template(fp.read())
        return template.render(news_list=news_list)

    def write_to_file(self, content):
        """This method write news to file"""
        try:
            with open(self.full_path_to_file, "wb") as fp:
                fp.write(content)
        except PermissionError:
            logging.error(
                "Conversion cannot be performed. Permission denied for this directory"
            )
            sys.exit()
        self.logger.info("News has been successfully converted")

    def process_news_list_with_images(self, news_list):
        """This method process list of news, replacing image links by local paths to images if they exist in local
        storage"""
        for item in news_list:
            try:
                filename = hashlib.md5(item.get("Image").encode()).hexdigest()
            except AttributeError:
                continue
            for existing_img in os.listdir(self.img_storage):
                if existing_img.split(".")[0] == filename:
                    item["Image"] = (self.img_storage / existing_img).resolve()
                    break
