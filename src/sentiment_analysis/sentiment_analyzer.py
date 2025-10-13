# ~/reddit_sentiment_tracker/src/sentiment_analysis/sentiment_analyzer.py

import logging
from typing import Dict
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

logger = logging.getLogger("reddit_sentiment_tracker")

# Initialize sentiment analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str) -> Dict[str, float]:
    """ Analyze text sentiment using VADER """
    try:
        return sentiment_analyzer.polarity_scores(text)
    except Exception as e:
        logger.error(f"Error getting polarity scores: {e}", exc_info=True)
        return {}
