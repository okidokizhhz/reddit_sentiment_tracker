# ~/reddit_sentiment_tracker/tests/test_sentiment_analyzer.py

from src.sentiment_analysis.sentiment_analyzer import analyze_sentiment

def test_analyze_sentiment():
    """ Test if an input string returns a dictionary """
    input_text = "This is a test string"
    result = analyze_sentiment(input_text)

    assert isinstance(result, dict)

def test_analyze_sentiment_empty_string():
    """ Test if an empty input string still returns a dict """
    input_text = ""
    result = analyze_sentiment(input_text)

    assert isinstance(result, dict)

def test_analyze_sentiment_key_strings():
    """ Test if an input string returns a dict with keys of the data type string """
    input_text = "This is amazing"
    result = analyze_sentiment(input_text)

    for key in result.keys():
        assert isinstance(key, str)

def test_analyze_sentiment_value_floats():
    """ Test if an input string returns a dict with values of the data type float """
    input_text = "This is amazing"
    result = analyze_sentiment(input_text)

    for value in result.values():
        assert isinstance(value, float)
        
def test_analyze_sentiment_positive_sentiment():
    """ Test if a positive sentiment string returns positive sentiment scores """
    input_text = "This is amazing"
    result = analyze_sentiment(input_text)

    overall_score = result.get("compound")    # the key "compound" represents the overall sentiment score

    if overall_score is not None:
        assert overall_score >= 0

def test_analyze_sentiment_negative_sentiment():
    """ Test if a negative sentiment string returns negative sentiment scores """
    input_text = "This is terrible"
    result = analyze_sentiment(input_text)

    overall_score = result.get("compound")    # the key "compound" represents the overall sentiment score

    if overall_score is not None:
        assert overall_score <= 0
