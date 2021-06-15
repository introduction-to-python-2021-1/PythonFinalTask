import logging
import os
from datetime import datetime

from PIL import Image
from fpdf import FPDF
from jinja2 import Template


class Converter:
    def __init__(self, convert_type, path):
        self.convert_type = convert_type
        self.path = path
        self.mapping = {
            "html": self.to_html,
            "pdf": self.to_pdf
        }

    def execute(self, content):
        """
            Parameters:
                content: list of dicts with news parameters(pubdate, title, link, image(url))
            Return the method(content)
        """
        self.mapping[self.convert_type](content)

    def to_html(self, content):
        """
            Convert content to HTML file
            Parameters:
                content: list of dicts with news parameters(pubdate, title, link, image(url))
            Return the HTML file
        """
        path_to_file = os.path.join(self.path, "converted_news", f"converted_to_html{str(datetime.now().date())}.html")
        with open(os.path.join(self.path, "templates", "template.html")) as f:
            template = Template(f.read())
        with open(path_to_file, "w") as f:
            f.write(template.render(content=content))
        logging.info("News converted to HTML-format")

    def to_pdf(self, content):
        """
            Convert content to PDF file
            Parameters:
                content: list of dicts with news parameters(pubdate, title, link, image(url))
            Return the PDF file
        """
        path_to_file = os.path.join(self.path, "converted_news", f"converted_to_pdf{str(datetime.now().date())}.pdf")
        pdf = FPDF()
        pdf.core_fonts_encoding = "utf-8"
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        for news in content:
            pubdate = news["pubdate"]
            title = news["title"]
            link = news["link"]
            pdf.cell(200, 10, txt=pubdate, ln=1, align="L")
            pdf.cell(200, 10, txt=title, ln=1, align="L")
            pdf.cell(200, 10, txt=link, ln=1, align="L", link=link)
            if image_path := news.get("image_path"):
                pdf.image(Image.open(image_path), x=10, w=80, link=link)
        pdf.output(path_to_file)
        logging.info("News converted to PDF-format")
