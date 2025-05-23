# ~/reddit_sentiment_tracker/reddit_sentiment_tracker/src/storage/schema_manager.py
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import (Column, Table,
                        String, Integer, Float, DateTime, Text)
from connection import metadata

# Schema/Table definitions
# Top Posts
top_posts = Table(
    'top_posts', metadata,
    Column('id', Integer, primary_key=True),
    Column('post_id', Integer, nullable=False),
    Column('author', String(100)),
    Column('created_utc', String(100), nullable=False),
    Column('num_comments', Integer),
    Column('url', String(500)),
    Column('awards', DateTime),
    Column('edited', DateTime),
    Column('flair', String(100)),
    Column('title', String(500)),
    Column('title_sentiment', JSONB),
    Column('selftext', Text),
    Column('body_sentiment', JSONB),
    Column('score', Integer),
    Column('upvote_ratio', Float),
    Column('controversiality', Float),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('last_updated', DateTime, onupdate=datetime.utcnow),
    Column('comments', JSONB)
)

# Rising Posts
rising_posts = Table(
    'rising_posts', metadata,
    Column('id', Integer, primary_key=True),
    Column('post_id', Integer, nullable=False),
    Column('author', String(100)),
    Column('created_utc', String(100), nullable=False),
    Column('num_comments', Integer),
    Column('url', String(500)),
    Column('awards', DateTime),
    Column('edited', DateTime),
    Column('flair', String(100)),
    Column('title', String(500)),
    Column('title_sentiment', JSONB),
    Column('selftext', Text),
    Column('body_sentiment', JSONB),
    Column('score', Integer),
    Column('upvote_ratio', Float),
    Column('controversiality', Float),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('last_updated', DateTime, onupdate=datetime.utcnow),
    Column('comments', JSONB)
)
