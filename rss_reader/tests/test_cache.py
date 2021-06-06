import filecmp

from rss_reader.tests.testing import BaseTest


class TestRssReader(BaseTest):
    def test_cache_news(self):
        """Tests that news is cached to a file"""
        self.cache.cache_news(self.example_news_list[0])
        self.assertTrue(
            filecmp.cmp(self.data_folder + 'cached_news.json', self.cache_folder + '20210505.json'))

    def test_get_news_from_cache(self):
        """Tests that news are correctly fetched from the cache"""
        self.cache.cache_news(self.example_news_list[0])
        feeds_list = self.cache.get_news_from_cache('20210505', None, None, False, False)
        self.assertEqual(feeds_list[0].news_list[0].to_dict(), self.example_news_list[0].to_dict())

    def test_get_news_from_cache_with_limit(self):
        """Tests that the --limit argument affects the news feed fetched from the cache"""
        for example_news in self.example_news_list:
            self.cache.cache_news(example_news)
        feeds_list = self.cache.get_news_from_cache('20210505', None, 2, False, False)
        self.assertEqual(len(feeds_list[0].news_list), 2)

    def test_get_news_from_cache_with_json(self):
        """Tests that the --json argument affects the news feed fetched from the cache"""
        for example_news in self.example_news_list:
            self.cache.cache_news(example_news)
        feeds_list = self.cache.get_news_from_cache('20210505', 'https://www.yahoo.com/news', None, True, False)
        with open(self.data_folder + 'result_json_5.json', 'r') as file:
            json_data = file.read()
        self.assertEqual(str(feeds_list[0]), json_data)

    def test_get_news_from_cache_with_json_and_limit(self):
        """Tests that the --json and --limit argument affects the news feed fetched from the cache"""
        for example_news in self.example_news_list:
            self.cache.cache_news(example_news)
        feeds_list = self.cache.get_news_from_cache('20210505', 'https://www.yahoo.com/news', 2, True, False)
        with open(self.data_folder + 'result_json_2.json', 'r') as file:
            json_data = file.read()
        self.assertEqual(str(feeds_list[0]), json_data)
