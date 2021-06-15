from rss_reader.xml_downloader import XmlDownloader
import unittest
import requests_mock


class TestXmlDownloader(unittest.TestCase):

    @requests_mock.mock()
    def test_xml_delivery(self, m):
        url = "https://www.buzzfeed.com/world.xml"
        xml = "<?xml version='1.0' encoding='UTF-8'?>"
        m.get(url, text=xml)

        rss_feed = XmlDownloader(url)
        self.assertEqual(rss_feed.xml, xml, "XML download malfunction")

    @requests_mock.mock()
    def test_error_code_handling(self, m):
        url = "https://www.buzzfeed.com/world.xml"
        xml = "<?xml version='1.0' encoding='UTF-8'?>"
        err_code = 403  # Forbidden
        m.get(url, text=xml, status_code=err_code)

        rss_feed = XmlDownloader(url)
        self.assertEqual(rss_feed.xml, "", "error handling malfunction")

    def test_invalid_url(self):
        url = ""
        self.rss_feed = XmlDownloader(url)
        expected_xml = ""

        self.assertEqual(self.rss_feed.xml, expected_xml, "Exception not raised")
