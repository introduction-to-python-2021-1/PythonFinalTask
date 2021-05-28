"""
This module provides funcs for converting feed to pdf format
"""

from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import time
from rss_reader_files import str_funcs

pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf'))


def convert_to_pdf(feed, path):
    """
    Convert feed to html format
    """
    parts = []
    try:
        for item in feed.items:
            result_str = (f'<br/> Title: {item.title} <br/> '
                          f'Link: {item.link} <br/> '
                          f'Date: {time.strftime("%y-%m-%d %H:%M", item.date)} <br/>')
            result_str += str_funcs.get_str_content(item.content) + '<br/>'
            stylesheet = getSampleStyleSheet()
            custom_style = ParagraphStyle('DejaVuSerif', fontName='DejaVuSerif')
            parts.append(Paragraph(result_str, style=custom_style))
            for img in item.img:
                images_as_str = f'Image: <img src={img["src"]} valign="top" width=100 height=100 />'
                parts.append(Paragraph(images_as_str, style=stylesheet['Normal']))
                parts.append(Spacer(width=100, height=100))
    except Exception as err:
        print(err)
    summaryName = SimpleDocTemplate(path)
    summaryName.build(parts)
