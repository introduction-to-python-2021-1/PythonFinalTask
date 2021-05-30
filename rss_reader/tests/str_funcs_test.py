import unittest
from rss_reader import str_funcs


class StringFunctionsTest (unittest.TestCase):
    def test_get_str_content(self):
        list_with_content = ['text']
        pretty_str = 'Content: \ntext'
        self.assertEqual('', str_funcs.get_str_content([]))
        self.assertEqual(pretty_str, str_funcs.get_str_content(list_with_content))

    def test_get_img_as_str(self):
        list_with_img = [{'src': 'test_src', 'alt': 'test_alt'}]
        pretty_str = '\nImage № 1: test_src\nDescription: test_alt'
        self.assertEqual('', str_funcs.get_img_as_str([]))
        self.assertEqual(pretty_str, str_funcs.get_img_as_str(list_with_img))

    def test_get_links_as_str(self):
        list_with_links = ['link 1', 'link 2']
        pretty_str = '\nLinks: \nlink 1\nlink 2'
        self.assertEqual('', str_funcs.get_links_as_str([]))
        self.assertEqual(pretty_str, str_funcs.get_links_as_str(list_with_links))

    def test_get_links(self):
        list_with_links = [{'type': 'text', 'href': 'link'}]
        list_with_clean_data = ['link']
        self.assertEqual('', str_funcs.get_links([]))
        self.assertEqual(list_with_clean_data, str_funcs.get_links(list_with_links))
