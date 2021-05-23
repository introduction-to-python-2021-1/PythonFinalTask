import unittest
from rss_reader.rss_reader import get_response, extract_xml


class Test_rss_reader(unittest.TestCase):
    url1 = "https://www.theguardian.com/world/rss"
    url2 = "https://news.yahoo.com/rss/"
    url3 = "https://.com/rss/"

    def test_get_response(self):
        self.assertTrue(get_response(self.url1))
        self.assertTrue(get_response(self.url2))
        self.assertFalse(get_response(self.url3))

    def test_extract_xml(self):
        with open("rss-test-theguardian.xml", "r") as file:
            content = file.read()
            print(len(extract_xml(content, 0)["News"]))
        self.assertIsInstance(extract_xml(content, 0), dict)
        self.assertEqual(len(extract_xml(content, 0)["News"]), 41)

if __name__ == "__main__":
    unittest.main()
