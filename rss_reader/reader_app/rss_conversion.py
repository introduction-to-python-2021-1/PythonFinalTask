import os

from fpdf import FPDF
from jinja2 import Environment, FileSystemLoader


class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', '', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f'Page {self.page_no()} of {{nb}}', 0, 0, align='C')


def print_to_pdf(news_dict, real_work_dir, file_path):
    """
    Function prints news dictionary to pdf file, puts in 'local_storage' folder.
    :param news_dict: (dict)
    :param real_work_dir: (str) path to 'rss_reader' directory
    :param file_path: (str) file name to print pdf
    :return: None
    """
    pdf = PDF('P', 'mm', 'A4')
    pdf.alias_nb_pages()
    pdf.set_doc_option('core_fonts_encoding', 'windows-1252')
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    # Heading
    pdf.set_font('helvetica', '', 16)
    pdf.cell(50, 15, txt="Feed:")
    pdf.cell(0, 15, txt=f"{news_dict['Feed']}", ln=True)
    pdf.cell(50, 15, txt="Items count:")
    pdf.cell(0, 15, txt=f"{news_dict['Items count']}", ln=True)
    # News items
    for item in news_dict['Items']:
        pdf.set_font('helvetica', '', 12)
        pdf.cell(0, 10, ln=True)
        # print image if exists
        if item['Image']['Path']:
            pdf.image(item['Image']['Path'], x=40, w=80)
        else:
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, txt='Image not available', align='C', ln=True)
        # print text
        for key, value in item.items():
            if key == 'Link' or key == 'Image':  # skip Link or Image
                continue
            pdf.set_font('helvetica', 'B', 12)
            pdf.set_text_color(0, 0, 0)
            website_link = item['Link']
            # category (key)
            pdf.cell(30, 10, txt=f'{key}:')
            # text (value)
            if key == 'Source':  # put website link
                pdf.set_font('courier', 'U', 12)
                pdf.set_text_color(0, 0, 255)
                src_val = value.encode('latin-1', 'ignore').decode('latin-1')
                pdf.multi_cell(0, 10, align='L', txt=src_val, link=website_link, ln=True)
            else:
                pdf.set_font('helvetica', '', 12)
                txt_multi_cell = value.encode('latin-1', 'ignore').decode('latin-1')
                pdf.multi_cell(0, 10, align='L', txt=txt_multi_cell, ln=True)
    # print to pdf
    pdf.output(os.path.join(real_work_dir, 'local_storage', file_path))


def print_to_html(news_dict, real_work_dir, file_path):
    """
    Function takes news dictionary and html path and converts dictionary to html file.
    :param news_dict: (dict)
    :param real_work_dir: (str) path to 'rss_reader' directory
    :param file_path: (str) file name to print html
    :return: None
    """
    # determine path to 'templates' directory
    tpl_dir = os.path.join(real_work_dir, 'local_storage', 'templates')

    # update (shorten) image name for insertion into template
    for item in news_dict['Items']:
        if item['Image']['Path']:
            item['Image']['Html Template Path'] = os.path.join('images', os.path.basename(item['Image']['Path']))
        else:
            item['Image']['Html Template Path'] = None

    file_loader = FileSystemLoader(tpl_dir)
    env = Environment(loader=file_loader)
    rendered = env.get_template('rss_template.html').render(news_items=news_dict['Items'],
                                                            title='Yahoo News - Latest News & Headlines')

    with open(os.path.join(real_work_dir, 'local_storage', file_path), 'w') as f_obj:
        f_obj.write(rendered)
