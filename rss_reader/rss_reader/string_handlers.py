"""
This module provides tools for presentation parts of news in readable format
"""


def get_str_content(list_with_content):
    """
    Return readable content
    """
    if not list_with_content:
        return ''
    pretty_str = f'Content: '
    for record in list_with_content:
        pretty_str += '\n' + record
    return pretty_str


def get_img_as_str(list_with_img):
    """
    Takes list with images and return it in readable format
    """
    if not list_with_img:
        return ''
    pretty_str = ''
    for num, img in enumerate(list_with_img):
        images_as_str = '\n' + f'Image № {str(num + 1)}: {img["src"]}'
        pretty_str += images_as_str
        if img['alt']:
            img_desc = f'Description: {img["alt"]}'
            pretty_str += '\n' + img_desc
    return pretty_str


def get_links_as_str(list_with_links):
    """
    Takes list containing links and return it in readable format
    """
    if not list_with_links:
        return ''
    pretty_str = '\nLinks: '
    for link in list_with_links:
        pretty_str += '\n' + link
    return pretty_str


def get_links(list_with_uncleaned_links):
    """
    Trying to get clean links and put them into list
    """
    if not list_with_uncleaned_links:
        return ''
    clean_data = []
    for link in list_with_uncleaned_links:
        clean_data.append(link['href'])
    return clean_data
