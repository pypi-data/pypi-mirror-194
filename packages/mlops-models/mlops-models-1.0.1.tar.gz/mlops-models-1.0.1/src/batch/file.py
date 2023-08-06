"""
Batch processing module

A CLI command that accepts an input file as an argument, classifies sentiment of each tweet in the file,
and writes the results to an output file
"""

import argparse
import json

from src.mlops_models.sentiment import TweetSentiment


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Input file path', required=True)
    parser.add_argument('--output', help='Output file path', required=True)
    args = parser.parse_args()

    model = TweetSentiment()

    with open(args.input, 'r') as f:
        input_lines = f.read().splitlines()

    data = []
    for tweet in input_lines:
        data.append(
            {"text": tweet,
             "sentiment": model.predict(tweet)}
        )

    with open(args.output, 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    main()
