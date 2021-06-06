"""
This module provides tests for image handlers
"""


import unittest
from rss_reader import image_handlers


class TestLinkCheck(unittest.TestCase):
    """
    Tests function that checks if image is link
    """
    def setUp(self) -> None:
        self.list_with_links = [{'type': 'image/jpeg', 'href': 'href', 'alt': 'alt'}]

    def test_if_img_is_link(self):
        """
        Test building a list of links leading to images
        """
        self.assertEqual(image_handlers.if_link_is_image(self.list_with_links), [{'src': 'href', 'alt': 'alt'}])
