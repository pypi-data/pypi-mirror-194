import os


class TweetSentiment:
    """
    This class is used to predict the sentiment of a tweet.
    """
    def __init__(self):

        model_path = os.path.join(
            os.path.dirname(__file__),
            "resources", "models"
        )
        self.positive = self._load_file_(os.path.join(model_path, "sentiment-positive-en.txt"))
        self.negative = self._load_file_(os.path.join(model_path, "sentiment-negative-en.txt"))


    def predict(self, text: str) -> int:
        """
        Predict the sentiment of a tweet.

        Compare words in text with positive and negative words, return 1 if more positive words than negative words,
        return -1 if more or equal negative words than positive words.
        Return 0 if no positive or negative words are found.

        :param text: The text of the tweet.
        :return: 1 if the tweet is positive, -1 if the tweet is negative, 0 if the tweet is neutral.
        """

        text = self._data_cleaning_(text)

        positive = 0
        negative = 0
        for word in text.split():
            if word in self.positive:
                positive += 1
            if word in self.negative:
                negative += 1
        if positive == 0 and negative == 0:
            return 0

        if positive > negative:
            return 1

        return -1

    def _data_cleaning_(self, text: str) -> str:
        """
        Clean the text of the tweet.
        :param text:
        :return:
        """
        # remove punctuation, exlamation marks, etc.
        for char in text:
            if char in '''!()-[]{};:'"\,<>./?@#$%^&*_~''':
                text = text.replace(char, "")

            if char in "0123456789":
                text = text.replace(char, "")

        # transform to lower case
        text = text.lower()

        return text


    def _load_file_(self, path: str) -> str:
        """
        Load a file from the resources folder.
        :param path:
        :return:
        """
        with open(path, "r") as f:
            return f.read()