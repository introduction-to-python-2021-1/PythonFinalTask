"""This module contains a class containing methods for converting news feed into various formats"""

from datetime import datetime
import glob
import hashlib
import imghdr
import os
import re
import urllib.error
import urllib.request

from jinja2 import Environment, PackageLoader
from xhtml2pdf import pisa


class Converter:
    """This class is needed for news feed conversion"""

    def __init__(self, logger):
        """
        This class constructor initializes the required variables for the news feed conversion

        Parameters:
            logger (module): logging module
        """
        self.logger = logger
        self.cache_folder_path = 'cache' + os.path.sep
        self.cache_images_folder_path = self.cache_folder_path + 'images' + os.path.sep

    def to_pdf(self, path, feeds_list, news_limit):
        """
        This method converts news feed to PDF format

        Parameters:
            path (str): Output filepath
            feeds_list (list): List of objects of class Feed
            news_limit (int or NoneType): Value that limits the number of news
        """
        self.logger.info(' Start converting news feed to PDF format')
        output_filepath = self.prepare_output_filepath(path, pdf=True)
        if output_filepath:
            try:
                with open(output_filepath, 'w+b') as file:
                    pisa.CreatePDF(self.to_html(feeds_list, news_limit, pdf=True), file, )
                    self.logger.info(f' PDF file created and saved at {output_filepath}')
            except PermissionError:
                self.logger.error(
                    f' Unable to save PDF file at {output_filepath}. Permission denied.')

    def __get_image(self, url, cached_image_filename):
        """
        This method tries to get image by filepath or link

        Parameters:
            url (str): Link to image
            cached_image_filename (str): Image filename

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

    def to_html(self, feeds_list, news_limit, path=None, pdf=False):
        """
        This method converts news feed to HTML format

        Parameters:
            feeds_list (list): List of objects of class Feed
            news_limit (int or NoneType): Value that limits the number of news
            path (str): Output filepath
            pdf (bool): If True prepares HTML for conversion to PDF

        Returns:
            str: HTML code required to get PDF if pdf is True
        """
        self.logger.info(' Start converting news feed to HTML format')
        env = Environment(loader=PackageLoader('components', 'templates'))
        env.filters['news_description_to_html'] = self.news_description_to_html
        env.filters['news_enclosures_to_html'] = self.news_enclosures_to_html
        env.filters['news_media_content_to_html'] = self.news_media_content_to_html
        template = env.get_template('template.html')
        news_list = []
        for feed in feeds_list:
            news_list += feed.news_list
        if pdf:
            return template.render(news_list=news_list[:news_limit],
                                   fonts=os.path.join(os.path.dirname(__file__), 'fonts'))
        else:
            output_filepath = self.prepare_output_filepath(path, html=True)
            if output_filepath:
                try:
                    with open(output_filepath, 'w') as file:
                        file.write(template.render(news_list=news_list[:news_limit], ))
                        self.logger.info(f' HTML file created and saved as {output_filepath}')
                except PermissionError:
                    self.logger.error(
                        f' Unable to save HTML file at {output_filepath}. Permission denied.')

    def prepare_output_filepath(self, path, pdf=False, html=False):
        """
        This method is needed to format the output filepath

        Parameters:
            path (str): Output filepath
            pdf (bool): If True appends .pdf to filename (if not specified)
            html (bool): If True appends .html to filename (if not specified)

        Returns:
            str: Formatted output filepath
            None: If permission denied
        """
        output_path, output_file_extension = os.path.splitext(path.rstrip(os.sep))
        if not output_file_extension and pdf:
            output_filename = f'{datetime.now()}.pdf'
        elif not output_file_extension and html:
            output_filename = f'{datetime.now()}.html'
        else:
            output_filename = f'{output_path.split(os.sep)[-1]}{output_file_extension}'
            output_path = f'{os.sep}'.join(output_path.split(os.sep)[:-1])
        if output_path:
            output_path += os.sep
            if not os.path.exists(output_path):
                try:
                    os.makedirs(output_path, exist_ok=True)
                except PermissionError:
                    self.logger.error(f' Unable to create directory {output_path}. Permission denied.')
                    return None
        return output_path + output_filename

    def news_description_to_html(self, news):
        """
        This method is needed to convert the news description to HTML format

        Parameters:
            news (News): Object of class News

        Returns:
            str: News description converted to HTML format
        """
        news_description = ''
        temp_index = 0
        images = list(re.finditer(r'\[image \d: .+\]', news.description))
        for image in images:
            news_description += news.description[temp_index:image.start()].strip()
            image_index = re.search(r' \d:', image.string).group(0)[1:2]
            cached_image_filename = f'{hashlib.md5(news.link.encode()).hexdigest()}_{image_index}'
            cached_image_file_path = self.__get_image(news.links[image_index]['url'], cached_image_filename)
            if cached_image_file_path:
                image_src = cached_image_file_path
            else:
                image_src = news.links[image_index]['url']
            image_alt = news.links[image_index]['attributes']['alt']
            news_description += f'<img src="{image_src}" alt="[{image_index}] {image_alt}">'
            temp_index = image.end()
        news_description += f'{news.description[temp_index:].strip()}\n\n'
        return news_description

    def news_enclosures_to_html(self, news):
        """
        This method is needed to convert the news enclosures to HTML format

        Parameters:
            news (News): Object of class News

        Returns:
            str: News enclosures converted to HTML format
        """
        news_enclosure_html = ''
        enclosure_indexes_list = []
        for link_index, link in news.links.items():
            if link['enclosure']:
                enclosure_indexes_list.append(link_index)
        if enclosure_indexes_list:
            news_enclosure_html += 'Enclosures:\n' + self.__links_to_html(news, enclosure_indexes_list)
        return news_enclosure_html

    def news_media_content_to_html(self, news):
        """
        This method is needed to convert the news media:content to HTML format

        Parameters:
            news (News): Object of class News

        Returns:
            str: News media:content converted to HTML format
        """
        news_media_content_html = ''
        media_content_indexes_list = []
        for link_index, link in news.links.items():
            if link['media']:
                media_content_indexes_list.append(link_index)
        if media_content_indexes_list:
            news_media_content_html += 'Media:\n' + self.__links_to_html(news, media_content_indexes_list)
        return news_media_content_html

    def __links_to_html(self, news, links):
        """
        This method is needed to convert the news links to HTML format

        Parameters:
            news (News): Object of class News
            links (list): List of news link indexes to be converted to HTML format

        Returns:
            str: Links converted to HTML format
        """
        news_links_html = ''
        for link_index in links:
            link = news.links[link_index]
            if 'image' in link['type']:
                cached_image_filename = f'{hashlib.md5(news.link.encode()).hexdigest()}_{link_index}'
                cached_image_file_path = self.__get_image(link['url'], cached_image_filename)
                if cached_image_file_path:
                    news_links_html += f'<img src="{cached_image_file_path}">'
                else:
                    news_links_html += f'[{link_index}]: {link["url"]} ({link["type"]})'
                news_links_html += '\n'
            else:
                news_links_html += f'[{link_index}]: {link["url"]} ({link["type"]})\n'
        return news_links_html
