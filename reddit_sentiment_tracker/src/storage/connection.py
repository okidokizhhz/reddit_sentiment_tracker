# ~/reddit_sentiment_tracker/reddit_sentiment_tracker/src/storage/connection.py
import os
from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv
from schema_manager import rising_posts, top_posts

# getting evironmental variables for db authentication
load_dotenv()
HOST_DB = os.getenv("HOST_DB")
NAME_DB = os.getenv("NAME_DB")
USER_DB = os.getenv("USER_DB")
PASSWORD_DB = os.getenv("PASSWORD_DB")
PORT_DB = os.getenv("PORT_DB")

# Setup, Connection to postgresql
engine = create_engine(f"postgresql://{USER_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}",
                        pool_size=5, max_overflow=10, pool_pre_ping=True)

# metadata object to hold table definitions
metadata = MetaData()

rising_posts = rising_posts
top_posts = top_posts

# Create all tables (run once)
def initialize_database():
    """Creates all defined tables in the database"""
    metadata.create_all(engine)
