# ~/reddit_sentiment_tracker/src/storage/schema_manager.py

from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import (Column, ForeignKey, Table,
                        String, Integer, Float, DateTime, Text)
from .connection import metadata

subreddits = Table(
    'subreddits', metadata,
    Column('id', String, primary_key=True),
    Column('name', String, unique=True, nullable=False),
    Column('description', Text, nullable=True),
    Column('subscriber_count', Integer, nullable=True),
    Column('created_utc', DateTime,  nullable=False),
    Column('fetched_at', DateTime, default=datetime.now(timezone.utc), nullable=False, index=True)   # index for time based queries

)

posts = Table(
    'posts', metadata,
    Column('id', String, primary_key=True),
    Column('subreddit_id', String, ForeignKey('subreddits.id'), nullable=False, index=True),  # index for subreddit id
    Column('author', String),
    Column('post_type', String, nullable=False),
    Column('title', String(500), nullable=False),
    Column('selftext', Text),
    Column('url', String),
    Column('flair', String),
    Column('created_utc', DateTime, nullable=False),
    Column('fetched_at', DateTime, default=datetime.now(timezone.utc), nullable=False),
)

post_sentiment_history = Table(
    'post_sentiment_history', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('post_id', String, ForeignKey('posts.id'), nullable=False, index=True),    # index for post id
    Column('title_sentiment', JSONB),
    Column('body_sentiment', JSONB),
    Column('score', Integer),
    Column('upvote_ratio', Float),
    Column('controversiality', Float),
    Column('num_comments', Integer),
    Column('measured_at', DateTime, default=datetime.now(timezone.utc), nullable=False)
)

comments = Table(
    'comments', metadata,
    Column('id', String, primary_key=True),
    Column('post_id', String, ForeignKey('posts.id'), nullable=False, index=True),    # index for post id
    Column('parent_comment_id', String, ForeignKey('comments.id'), nullable=True, index=True),   # index for parent comment id
    Column('depth', Integer),
    Column('author', String),
    Column('text', Text),
    Column('score', Integer),
    Column('created_utc', DateTime, nullable=False, index=True),     # index for time based queries
    Column('fetched_at', DateTime, default=datetime.now(timezone.utc), nullable=False)
)    

comment_sentiment_history = Table(
    'comment_sentiment_history', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('comment_id', String, ForeignKey('comments.id'), nullable=False, index=True),  # index for comment id
    Column('comment_sentiment', JSONB),
    Column('score', Integer),
    Column('measured_at', DateTime, default=datetime.now(timezone.utc), nullable=False)
)

average_daily_sentiment = Table(
    'average_daily_sentiment', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('date', DateTime, nullable=False, index=True),
    Column('subreddit_id', String, ForeignKey('subreddits.id'), nullable=False, index=True),
    Column('average_post_sentiment', Float),
    Column('average_comment_sentiment', Float),
    Column('overall_sentiment', Float),
    Column('post_count', Integer),
    Column('comment_count', Integer),
    Column('calculated_at', DateTime, default=datetime.now(timezone.utc), nullable=False, index=True)
)
