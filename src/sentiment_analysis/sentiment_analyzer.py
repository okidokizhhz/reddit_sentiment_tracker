# ~/reddit_sentiment_tracker/src/sentiment_analysis/sentiment_analyzer.py

import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

logger = logging.getLogger("reddit_sentiment_tracker")

def analyze_sentiment(text):
    """ Analyze text sentiment using VADER """

    # Initialize sentiment analyzer once
    sentiment_analyzer = SentimentIntensityAnalyzer()

    return sentiment_analyzer.polarity_scores(text)
