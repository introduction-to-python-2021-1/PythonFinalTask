def get_str_content(list_with_content):
    if not list_with_content:
        return ''
    pretty_str = 'Content: '
    for record in list_with_content:
        pretty_str += '\n' + record
    return pretty_str


def get_img_as_str(list_with_img):
    if not list_with_img:
        return ''
    pretty_str = ''
    for num, img in enumerate(list_with_img):
        images_as_str = f'Image № {str(num + 1)}: {img["src"]}'
        pretty_str += images_as_str
        if img['alt']:
            img_desc = f'Description: {img["alt"]}'
            pretty_str += '\n' + img_desc
    return pretty_str


def get_links_as_str(list_with_links):
    if not list_with_links:
        return ''
    pretty_str = 'Links: '
    for link in list_with_links:
        pretty_str += '\n' + link
    return pretty_str


def get_links(links_list):
    if not links_list:
        return ''
    clean_data = []
    for link in links_list:
        clean_data.append(link['href'])
    return clean_data
