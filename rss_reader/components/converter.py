import os
import re
import hashlib
from datetime import datetime
import glob
import urllib.request
import urllib.error
import imghdr

import fpdf
from bs4 import BeautifulSoup


class Converter:
    """This class is needed for news feed conversion"""

    def __init__(self, logger):
        """This class constructor initializes the required variables for the news feed conversion"""
        self.logger = logger
        self.cache_folder_path = 'cache' + os.sep
        self.cache_images_folder_path = self.cache_folder_path + 'images' + os.path.sep

    def to_pdf(self, path, feed, limit):
        """This method converts news feed to PDF file"""
        self.logger.info(' Start converting news feed to PDF file')
        fpdf.set_global('SYSTEM_TTFONTS', os.path.join(os.path.dirname(__file__), 'fonts'))
        pdf = fpdf.FPDF()
        pdf.add_font('DejaVuSans', '', 'DejaVuSans.ttf', uni=True)
        pdf.set_font('DejaVuSans', size=12)
        for news in feed.news_list[:limit]:
            pdf.add_page()
            pdf.write(5, f'[{news.feed_title}] {news.title}\n', news.link)
            pdf.write(5, f'{news.formatted_date}\n\n')
            if news.description:
                temp_index = 0
                images = list(re.finditer(r'\[image \d: .+\]', news.description))
                for image in images:
                    pdf.write(5, news.description[temp_index:image.start()].strip())
                    image_index = re.search(' \d:', image.string).group(0)[1:2]
                    cached_image_filename = f'{hashlib.md5(news.link.encode()).hexdigest()}_{image_index}'
                    cached_image_file_path = self.__get_image(news.links[image_index]['url'], cached_image_filename)
                    if cached_image_file_path:
                        pdf.image(cached_image_file_path)
                    else:
                        pdf.write(5, f' {image.group(0)} ', news.links[image_index]['url'])
                    temp_index = image.end()
                pdf.write(5, news.description[temp_index:].strip() + '\n\n')
            enclosure_indexes_list = []
            for link_index, link in news.links.items():
                if link['enclosure']:
                    enclosure_indexes_list.append(link_index)
            if enclosure_indexes_list:
                pdf.write(5, 'Enclosures:\n')
                for enclosure_index in enclosure_indexes_list:
                    enclosure = news.links[enclosure_index]
                    if 'image' in enclosure['type']:
                        cached_image_filename = f'{hashlib.md5(news.link.encode()).hexdigest()}_{enclosure_index}'
                        cached_image_file_path = self.__get_image(enclosure['url'], cached_image_filename)
                        if cached_image_file_path:
                            pdf.image(cached_image_file_path, w=100)
                        else:
                            pdf.write(5, f'[{enclosure_index}]: {enclosure["url"]} ({enclosure["type"]})')
                        pdf.write(5, '\n')
                    else:
                        pdf.write(5, f'[{enclosure_index}]: {enclosure["url"]} ({enclosure["type"]})\n')
        result_path, result_file_extension = os.path.splitext(path.rstrip(os.sep))
        if not result_file_extension:
            result_filename = f'{datetime.now()}.pdf'
        else:
            result_filename = f'{result_path.split(os.sep)[-1]}{result_file_extension}'
            result_path = f'{os.sep}'.join(result_path.split(os.sep)[:-1])
        if result_path and not os.path.exists(result_path):
            os.makedirs(result_path, exist_ok=True)
        try:
            pdf.output(result_path + os.sep + result_filename)
            self.logger.info(f' PDF file created and saved at {result_path + os.sep + result_filename}')
        except PermissionError:
            self.logger.error(
                f' Unable to save PDF file at {result_path + os.sep + result_filename}. Permission denied.')

    def __get_image(self, url, cached_image_filename):
        """
        This method tries to get an image from a link if the news is cached but the image is not

        Returns:
            str: Image file path
            None: If it is not possible to download the image from the link
        """
        cached_image_file_path = glob.glob(os.path.join(self.cache_images_folder_path, f'{cached_image_filename}.*'))
        if not cached_image_file_path:
            self.logger.error(f' Could not find image with file name "{cached_image_filename}".')
            self.logger.info(f' Trying to get image from link')
            cached_image_file_path = self.cache_images_folder_path + cached_image_filename
            try:
                urllib.request.urlretrieve(url, cached_image_file_path)
                image_format = imghdr.what(cached_image_file_path)
                os.rename(cached_image_file_path, f'{cached_image_file_path}.{image_format}')
                return os.path.abspath(f'{cached_image_file_path}.{image_format}')
            except urllib.error.URLError:
                self.logger.error(' Unable to get image from link')
                return None
        else:
            return os.path.abspath(cached_image_file_path[0])

    def to_html(self, path, feed, limit):
        """This method converts news feed to HTML file"""
        self.logger.info(' Start converting news feed to HTML file')
        news_html_containers = []
        for news in feed.news_list:
            news_description = ''
            news_enclosure = ''
            if news.description:
                temp_index = 0
                images = list(re.finditer(r'\[image \d: .+\]', news.description))
                for image in images:
                    news_description += news.description[temp_index:image.start()].strip()
                    image_index = re.search(' \d:', image.string).group(0)[1:2]
                    cached_image_filename = f'{hashlib.md5(news.link.encode()).hexdigest()}_{image_index}'
                    cached_image_file_path = self.__get_image(news.links[image_index]['url'], cached_image_filename)
                    if cached_image_file_path:
                        image_src = cached_image_file_path
                    else:
                        image_src = news.links[image_index]['url']
                    news_description += f'<img src="{image_src}">'
                    temp_index = image.end()
                news_description += f'{news.description[temp_index:].strip()}\n\n'
            enclosure_indexes_list = []
            for link_index, link in news.links.items():
                if link['enclosure']:
                    enclosure_indexes_list.append(link_index)
            if enclosure_indexes_list:
                news_enclosure += 'Enclosures:\n'
                for enclosure_index in enclosure_indexes_list:
                    enclosure = news.links[enclosure_index]
                    if 'image' in enclosure['type']:
                        cached_image_filename = f'{hashlib.md5(news.link.encode()).hexdigest()}_{enclosure_index}'
                        cached_image_file_path = self.__get_image(enclosure['url'], cached_image_filename)
                        if cached_image_file_path:
                            news_enclosure += f'<img src="{cached_image_file_path}">'
                        else:
                            news_enclosure += f'[{enclosure_index}]: {enclosure["url"]} ({enclosure["type"]})'
                        news_enclosure += '\n'
                    else:
                        news_enclosure += f'[{enclosure_index}]: {enclosure["url"]} ({enclosure["type"]})\n'
            news_html_container = f'<div><h4><a href="{news.link}">[{news.feed_title}] {news.title}</a></h4>\n' \
                                  f'<p>{news.formatted_date}</p>\n\n' \
                                  f'{"<p>" + news_description + "</p>" if news_description else ""}' \
                                  f'{"<p>" + news_enclosure + "</p>" if news_enclosure else ""}</div>'
            news_html_containers.append(news_html_container)
        result_path, result_file_extension = os.path.splitext(path.rstrip(os.sep))
        if not result_file_extension:
            result_filename = f'{datetime.now()}.html'
        else:
            result_filename = f'{result_path.split(os.sep)[-1]}{result_file_extension}'
            result_path = f'{os.sep}'.join(result_path.split(os.sep)[:-1])
        if result_path and not os.path.exists(result_path):
            os.makedirs(result_path, exist_ok=True)
        result_feed_html = ''.join(news_html_containers)
        soup = BeautifulSoup(f'<!DOCTYPE html><html><body>{result_feed_html}</body></html>', 'lxml')
        result_html = soup.prettify()
        try:
            with open(result_path + os.sep + result_filename, 'w') as file:
                file.write(result_html)
            self.logger.info(f' HTML file created and saved as {result_path + os.sep + result_filename}')
        except PermissionError:
            self.logger.error(
                f' Unable to save HTML file at {result_path + os.sep + result_filename}. Permission denied.')
