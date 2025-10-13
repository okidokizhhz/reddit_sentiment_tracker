# ~/reddit_sentiment_tracker/src/storage/schema_manager.py

from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import (Column, ForeignKey, Table,
                        String, Integer, Float, DateTime, Text, Boolean)
from connection import metadata
import logging

logger = logging.getLogger("reddit_sentiment_tracker")

# Schema/Table definitions
# Posts
posts = Table(
    'posts', metadata,
    Column('id', String, primary_key=True),
    Column('posts-type', String(100), nullable=False),
    Column('author', String(100)),
    Column('created_utc', String(100), nullable=False),
    Column('num_comments', Integer),
    Column('url', String(500)),
    Column('awards', Integer),
    Column('edited', Boolean),
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

# Comments
comments = Table(
    'comments', metadata,
    Column('id', String, primary_key=True),          # reddit comment id
    Column('parent_id', String(100), ForeignKey('posts.id')), # relation to posts id
    Column('depth', Integer),
    Column('author', String(100)),
    Column('text', Text),
    Column('score', Integer),
    Column('edited', Boolean),
    Column("created_utc", String(100)),
    Column('sentiment', JSONB),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('last_updated', DateTime, onupdate=datetime.utcnow)
)    
