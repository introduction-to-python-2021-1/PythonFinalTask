"""
This module provides functions for fetching and working with images
"""


import requests
from bs4 import BeautifulSoup


def get_img_container(link):
    """
    This function parses html page to find images related to feed
    :param link: html page
    :return: list with dicts representing image as link('src') and description('alt')
    """
    img_list = []
    request = requests.get(link)
    soup = BeautifulSoup(request.text, 'lxml')
    img_container = soup.find_all('div', class_='caas-img-container')
    for container in img_container:
        if container:
            img_dict = get_img_from_container(container)
            img_list.append(img_dict)
    return img_list


def get_img_from_container(img_container):
    """
    Looking through img container, looking for images
    :param img_container: container with images
    :return: dict containing info about image(src, alt)
    """
    for img in img_container.find_all('img'):
        clean_text = BeautifulSoup(img.get('alt'), "lxml").text
        if img.get('src'):
            img_dict = {'src': img.get('src'), 'alt': clean_text}
            return img_dict


def if_link_is_image(links_list):
    """
    This function checks if links are images
    :param links_list: list with links to check
    :return: list containing images links
    """
    img_list = []
    for link in links_list:
        if link['type'] == 'image/jpeg':
            img_list.append({'src': link.get('href', ''), 'alt': link.get('alt', '')})
    return img_list
