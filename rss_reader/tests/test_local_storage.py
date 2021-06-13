import unittest
from rss_reader import local_storage
from unittest import mock
class TestLocalSrorage(unittest.TestCase):
	pass
	# def test_file_not_found(self):
	# 	# local_st = local_storage.local_storage("not_existing.json")
	# 	with self.assertRaises(Exception): local_storage.local_storage.__init__("not_exist.file")
# @mock.patch("rss_reader.local_storage.")
# 	def test_get_news(self):
# 		local_st = local_storage.local_storage("fake_news.json")
# 		self.assertIsInstance(local_st.get_news_by_date_from_locale_storage(), list)
if __name__ == '__main__':
	unittest.main()