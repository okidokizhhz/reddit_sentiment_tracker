# ~/reddit_sentiment_tracker/reddit_sentiment_tracker/src/storage/connection.py
import os
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import (
    Column, create_engine, MetaData, Table,
    String, Integer, Float, DateTime, Text
)
from dotenv import load_dotenv

# getting evironmental variables for db authentication
load_dotenv()
HOST_DB = os.getenv("HOST_DB")
NAME_DB = os.getenv("NAME_DB")
USER_DB = os.getenv("USER_DB")
PASSWORD_DB = os.getenv("PASSWORD_DB")
PORT_DB = os.getenv("PORT_DB")

# Setup, Connection to postgresql
engine = create_engine(f"postgresql://{USER_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}")

# metadata object to hold table definitions
metadata = MetaData()

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

# Create all tables (run once)
def initialize_database():
    """Creates all defined tables in the database"""
    metadata.create_all(engine)
