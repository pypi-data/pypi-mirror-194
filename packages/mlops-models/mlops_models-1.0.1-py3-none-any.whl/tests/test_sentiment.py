import unittest

from src.mlops_models.sentiment import TweetSentiment


class TestTweetSentiment(unittest.TestCase):

	def test_positive(self):

		model = TweetSentiment()
		self.assertEqual(model.predict("Amazing, I love this"), 1)


	def test_negative(self):

		model = TweetSentiment()
		self.assertEqual(model.predict("This is chaos"), -1)


	def test_neutral(self):

		model = TweetSentiment()
		self.assertEqual(model.predict("what about that"), 0)



## To run the tests
# bash
# python -m unittest discover -s src/tests -p "test_*.py"