import requests
import os.path
from os import sep as os_sep
from xhtml2pdf import pisa


def save_pdf(data, input_path, date):
    path = r'{0}rss_feed_time {1}.pdf'.format(input_path + os_sep, date)
    img = False
    if not os.path.exists(input_path):
        os.makedirs(input_path)

    try:
        code = requests.get(data[0]['media'])
        img = True

    except requests.exceptions.ConnectionError:
        pass

    pdf_string = '''<Html>
                        <Head>
                            <title>RSS feed</title>
                        </Head>
                    <Body>
                '''

    with open(path, "w+b") as result_file:
        for i in data:
            pdf_string += '''
                <h3>{}</h1>
                <a href = {}>Feed URL</a>
                <p>Publication date: {}</p>
                {}
                <hr>
                '''.format(i['title'],
                           i['link'],
                           i['pubDate'],
                           f'<img src="{i["media"]}" height="344" width="520">' if img else 'Can\'t display image')
        pdf_string += '''
            </Body>
        </Html>
        '''
        pisa.CreatePDF(pdf_string, dest=result_file)

    print(f'File with news was created in path {path}')


def save_html(data, input_path, date):
    path = r'{0}rss_feed_time {1}.html'.format(input_path + os_sep, date)
    if not os.path.exists(input_path):
        os.makedirs(input_path)

    with open(path, 'w', encoding='utf-8') as file:
        file.write('''
        <Html>
            <Head>
                <title>RSS feed</title>
            </Head>
            <Body>
        ''')
        for i in data:
            file.write('''
                <h3>{}</h1>
                <a href = {}>Feed URL</a>
                <p>Publication date: {}</p>
                <img src="{}" height="344" width="520" alt="Can\'t display the image">
                <hr>
                '''.format(i['title'], i['link'], i['pubDate'], i['media']))
        file.write('''
            </Body>
        </Html>
        ''')

    print(f'File with news was created in path {path}')
