import feedparser
import collections
import time
import json
import os
import requests
from bs4 import BeautifulSoup


def get_img(link):
    img_list = []
    request = requests.get(link)
    soup = BeautifulSoup(request.text, 'lxml')
    img_container = soup.find_all('div', class_='caas-img-container')
    for container in img_container:
        if container:
            for img in container.find_all('img'):
                clean_text = BeautifulSoup(img.get('alt'), "lxml").text
                if img.get('src'):
                    img_dict = {'src': img.get('src'), 'alt': clean_text}
                    img_list.append(img_dict)
    return img_list


class RssParser:
    def __init__(self, url, limit):
        self.url = url
        self.limit = limit
        self.items = []
        self.name = ''

    def get_feed(self):
        data = feedparser.parse(self.url)
        if data['bozo']:
            raise ValueError("Please check URL and Internet connection")
        self.name = data['feed'].get('title')
        self.get_content(data)
        return self.items

    def get_content(self, data):
        for feed in data['entries'][:self.limit]:
            title = feed.get('title', 'Absence of title')
            link = feed.get('link', 'Absence of link')
            date = feed.get('published_parsed', 'Absence of date')
            img = get_img(link)
            summary_list = []
            links = []
            if feed.get('summary'):
                summary_list.append(feed.get('summary'))
            if feed.get('links'):
                links = feed.get('links')
                for link in links:
                    if link['type'] == 'image/jpeg':
                        img.append({'src': link.get('href', ''), 'alt': link.get('alt', '')})
            fields = 'title, link, date, img, content, links'
            item = collections.namedtuple('item', fields)._make((title, link, date, img, summary_list, links))
            self.save_feed_into_cache(item)
            self.items.append(item)

    # def if_links_is_image(self, links_list):


    def convert_to_json(self):
        return json.dumps({'url': self.url,
                           'feed': {'name': self.name,
                                    'items': [item._asdict() for item in self.items]}}, ensure_ascii=False)

    def save_feed_into_cache(self, item):
        date = time.strftime('%Y%m%d', item.date)
        dir_path = os.path.abspath(os.path.dirname(__file__)) + os.path.sep + 'feed_cache' + os.path.sep
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        file_path = dir_path + date + '.json'
        item_to_cache = json.dumps(item._asdict(), ensure_ascii=False)
        print('trying to open')
        with open(file_path, 'a', encoding='utf-8') as fp:
            if os.stat(file_path).st_size == 0:
                feed_list = [item_to_cache]
                json.dump(feed_list, fp)
                return
        with open(file_path, 'r', encoding='utf-8') as fp:
            feed_list = json.load(fp)
            if item_to_cache in feed_list:
                return
            feed_list.append(item_to_cache)
        with open(file_path, 'w', encoding='utf-8') as fp:
            json.dump(feed_list, fp)
        return

    def __str__(self):
        result_str = self.name + '\n'
        for item in self.items:
            item_as_str = (f'Title: {item.title}\nLink: {item.link["href"]}\n'
                           f'Date: {time.strftime("%y-%m-%d %H:%M", item.date)}\n')
            result_str += item_as_str
            if item.content:
                result_str += 'Content: ' + self.get_str_content(item.content)
            result_str += self.get_img_as_str(item.img)
            if item.links:
                result_str += 'Links: ' + self.get_links_as_str(item.links)
            result_str += '\n\n'
        return result_str

    def get_str_content(self, list_with_content):
        pretty_str = ''
        for record in list_with_content:
            pretty_str += record + '\n'
        return pretty_str

    def get_img_as_str(self, list_with_img):
        pretty_str = ''
        for num, img in enumerate(list_with_img):
            images_as_str = f'Image № {str(num + 1)}: {img["src"]}'
            pretty_str += images_as_str + '\n'
            if img['alt']:
                img_desc = f'Description: {img["alt"]}'
                pretty_str += img_desc + '\n'
        return pretty_str

    def get_links_as_str(self, list_with_links):
        pretty_str = ''
        for link in list_with_links:
            pretty_str += link['href'] + '\n'
        return pretty_str