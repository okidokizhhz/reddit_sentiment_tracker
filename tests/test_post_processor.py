# ~/reddit_sentiment_tracker/tests/test_post_processor.py

import pytest
from unittest.mock import Mock
from src.data_collection.post_processor import process_post

@pytest.fixture
def post_data():
    """ Reusable Post data (mimics reddit praw object) fixture """
    mock_post = Mock()
    mock_post.id = "33333"
    mock_post.author = "Karl"
    mock_post.created_utc = 1729519800
    mock_post.num_comments = 22
    mock_post.url = "https://reddit.com/r/wien"
    mock_post.all_awardings = []
    mock_post.edited = False
    mock_post.link_flair_text = "Rant"
    mock_post.title = "foodora mal wieder"
    mock_post.selftext = "foodora Fahrer rasen durch die Stadt. Sie halten sich nicht an Verkersregeln"
    mock_post.score = 15
    mock_post.upvote_ratio = 0.44

    return mock_post

def test_process_post_returns_dict(post_data):
    """ Test if process_post returns a dictionary """
    result = process_post(post_data)

    assert result is not None
    assert isinstance(result, dict)

def test_process_post_correct_fields(post_data):
    """ Test if fields are present and contain the proper values """
    result = process_post(post_data)

    if result is not None:
        assert result["id"] == "33333"
        assert result["author"] == "Karl"
        assert result["score"] == 15
        assert result["flair"] == "Rant"

def test_process_post_sentiment_scores(post_data):
    """ Test if sentiment scores are attached in post_data """
    result = process_post(post_data)

    assert "title_sentiment" in result
    assert "body_sentiment" in result

def test_process_post_sentiment_return_dict(post_data):
    """ Test if sentiment scores are returned in a dictionary """
    result = process_post(post_data)

    if result is not None:
        title_sentiment_value = result["title_sentiment"]
        body_sentiment_value = result["body_sentiment"]

        assert isinstance(title_sentiment_value, dict)
        assert isinstance(body_sentiment_value, dict)

def test_process_post_controversiality(post_data):
    """ Test if controversiality is calculated properly """
    result = process_post(post_data)

    test_controversiality_result = (1 - 0.44) * 22   # (1 - upvote_ratio) * num_comments

    if result is not None:
        assert result["controversiality"] == test_controversiality_result
