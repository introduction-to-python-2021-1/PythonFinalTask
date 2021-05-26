from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import time

pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf'))


def convert_to_pdf(feed, path):
    parts = []
    try:
        for item in feed.items:
            result_str = ''
            item_as_str = (f'Title: {item.title} <br/> '
                           f'Link: {item.link["href"]} <br/> '
                           f'Date: {time.strftime("%y-%m-%d %H:%M", item.date)} <br/>')
            result_str += item_as_str
            if item.content:
                result_str += 'Content: '
                for content in item.content:
                    result_str += content + '<br/>'
            stylesheet = getSampleStyleSheet()
            yourStyle = ParagraphStyle('DejaVuSerif', fontName='DejaVuSerif')
            parts.append(Paragraph(result_str, style=yourStyle))
            for img in item.img:
                images_as_str = f'Image: <img src={img["src"]} valign="top" width=100 height=100 />'
                parts.append(Paragraph(images_as_str, style=stylesheet['Normal']))
                parts.append(Spacer(width=100, height=100))
    except Exception as err:
        print(err)
    summaryName = SimpleDocTemplate(path)
    summaryName.build(parts)
