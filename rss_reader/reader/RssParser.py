import feedparser
from collections import namedtuple
import time
import json
import requests
from bs4 import BeautifulSoup
from reader.cache_handlers import save_feed_into_cache
from reader import str_funcs


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
                summary_list = [feed.get('summary')]
            if feed.get('links'):
                uncleaned_links = feed.get('links')
                links = str_funcs.get_links(uncleaned_links)
                img.extend(if_link_is_image(uncleaned_links))
            fields = 'title, link, date, img, content, links'
            item = namedtuple('item', fields)._make((title, link, date, img, summary_list, links))
            save_feed_into_cache(item)
            self.items.append(item)

    def convert_to_json(self):
        return json.dumps({'url': self.url,
                           'feed': {'name': self.name,
                                    'items': [item._asdict() for item in self.items]}}, ensure_ascii=False)

    def __str__(self):
        result_str = self.name + '\n'
        for item in self.items:
            print(item.link)
            item_as_str = (f'Title: {item.title}\nLink: {item.link}\n'
                           f'Date: {time.strftime("%y-%m-%d %H:%M", item.date)}')
            result_str += item_as_str
            result_str += str_funcs.get_str_content(item.content)
            result_str += str_funcs.get_img_as_str(item.img)
            result_str += str_funcs.get_links_as_str(item.links) + '\n\n'
        return result_str


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


def if_link_is_image(links_list):
    img_list = []
    for link in links_list:
        if link['type'] == 'image/jpeg':
            img_list.append({'src': link.get('href', ''), 'alt': link.get('alt', '')})
    return img_list
