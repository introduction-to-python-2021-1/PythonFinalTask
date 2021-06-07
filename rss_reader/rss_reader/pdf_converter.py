"""
This module provides funcs for converting feed to pdf format
"""


from reportlab import platypus
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import time
from rss_reader import string_handlers


pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf'))


def convert_to_pdf(feed, path):
    """
    Convert feed to pdf format
    :param feed: feed object
    :param path: directory where news.pdf file will be saved
    """
    parts = []
    custom_style = ParagraphStyle('DejaVuSerif', fontName='DejaVuSerif')
    try:
        for item in feed:
            result_str = item.name + '<br/>'
            result_str += (f'<br/> Title: {item.title} <br/> '
                           f'Link: <link href={item.link} color="blue">{item.link}</link> <br/> '
                           f'Date: {time.strftime("%y-%m-%d %H:%M", tuple(item.date))} <br/>')
            parts.append(platypus.Paragraph(result_str, style=custom_style))
            if item.img:
                for img in item.img:
                    parts.append(platypus.Paragraph(convert_img_list_to_pretty_str(img), style=custom_style))
                    parts.append(platypus.Spacer(width=150, height=150))
    except Exception as err:
        print(err)
    summaryName = platypus.SimpleDocTemplate(path)
    summaryName.build(parts)


def convert_img_list_to_pretty_str(img):
    """
    Convert image to readable string
    :param img: Image
    :return: Readable string which contains images
    """
    pretty_str = ''
    if img['alt']:
        img_desc = f'Description: {img["alt"]}'
        pretty_str += img_desc + '<br/>'
    images_as_str = f'Image: <img src={img["src"]} valign="top" width=150 height=150 />'
    pretty_str += images_as_str + '<br/>'
    return pretty_str
