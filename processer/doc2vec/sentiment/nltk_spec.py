import unittest
from processer.sentiment.nltk_analizer import NLTKAnalizer
class MyTestCase(unittest.TestCase):
    def test_basic(self):
        analizer = NLTKAnalizer()
        print(analizer.exec('this is a pen.'))
