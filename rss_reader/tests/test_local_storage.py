import io
import sys
import unittest

from rss_reader import local_storage

class TestLocalStorage(unittest.TestCase):
	def setUp(self):
		self.output = io.StringIO()
		sys.stdout = self.output

	def test_local_file_not_exist(self):
		argv = ["--date", "20210606"]
		with self.assertRaises(FileNotFoundError):
			ls_container = local_storage.local_storage(path="../tmp/news.json")