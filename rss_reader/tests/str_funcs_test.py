import unittest
from rss_reader import string_handlers


class TestStringMethods(unittest.TestCase):
    """
    Provides tests for strings formation
    """
    def test_content_as_string(self):
        """
        Tests if correct string is formed from list with content
        """
        list_with_content = ['text']
        pretty_str = '\nContent: \ntext'
        self.assertEqual('', string_handlers.get_str_content([]))
        self.assertEqual(pretty_str, string_handlers.get_str_content(list_with_content))

    def test_image_as_str(self):
        """
        Tests if correct string is formed from list with images
        """
        list_with_img = [{'src': 'test_src', 'alt': 'test_alt'}]
        pretty_str = '\nImage № 1: test_src\nDescription: test_alt'
        self.assertEqual('', string_handlers.get_img_as_str([]))
        self.assertEqual(pretty_str, string_handlers.get_img_as_str(list_with_img))

    def test_links_as_string(self):
        """
        Tests if correct string is formed from list with links
        """
        list_with_links = ['link 1', 'link 2']
        pretty_str = '\nLinks: \nlink 1\nlink 2'
        self.assertEqual('', string_handlers.get_links_as_str([]))
        self.assertEqual(pretty_str, string_handlers.get_links_as_str(list_with_links))

    def test_list_of_links_formation(self):
        """
        Tests if correct list is generated from list with uncleaned links
        """
        list_with_links = [{'type': 'text', 'href': 'link'}]
        list_with_clean_data = ['link']
        self.assertEqual('', string_handlers.get_links([]))
        self.assertEqual(list_with_clean_data, string_handlers.get_links(list_with_links))


if __name__ == '__main__':
    unittest.main()
