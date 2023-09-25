import unittest
from file_reader.newsgroup import load
class MyTestCase(unittest.TestCase):

    def test_loader(self):
        print(list(load('./example/newsgroup20')))
