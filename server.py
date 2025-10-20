# ~/reddit_sentiment_tracker/server.py

import sys
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from typing import Optional, Any, Dict, List

from fastapi import FastAPI

from src.logger import setup_logger
from src.storage.connection import initialize_database
from src.storage.crud import retrieve_metadata, retrieve_posts_data, retrieve_comments_data

logger = setup_logger("reddit_sentiment_tracker")

# lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """ handle startup, db initialization, shutdown """
    logger.info("Reddit Sentiment Tracker API starting up...")     # startup

    try:
        initialize_database()
        logger.info("Startup completed successfully")
    except Exception as e:
        logger.critical(f"Startup failed: {e}", exc_info=True)
        sys.exit(1)                                             # force shutdown if failure

    yield                                                               # app runs here between startup and shutdown

    logger.info("Reddit Sentiment Tracker API shutting down...")   # shutdown


# creating FastAPI Instance
app = FastAPI(
    title="Reddit Sentiment Tracker API",
    description="Reddit tracking System",
    version="1.0.0",
    lifespan=lifespan                                                   # passing the lifespan context manager to handle startup/shutdown
)


@app.get("/")                                                     # root
async def read_root():
    """ root """
    return {"message": "welcome to", "program": "reddit sentiment tracker"}


@app.get("/health")                                               # get request to /health
async def health_check():
    """ Health check endpoint for monitoring the API """
    return {
        "status": "healthy",
        "service": "Reddit Sentiment Tracker API",
        "timestamp": datetime.now(timezone.utc),
        "message": "API is running correctly",
        "environment": "development"
    }


@app.get("/subreddit_metadata/{subreddit_name}")                                   # get request to /subreddit_metadata with parameter
async def get_subreddit_metadata(subreddit_name: str):
    """ Get Subreddit Metadata (name, description, subscriber count, created at) endpoint """
    try:
        subreddit_metadata = retrieve_metadata(subreddit_name)

        if subreddit_metadata is None:
            logger.warning(f"No data for '{subreddit_name}' in DB found")
            return {"error": f"Subreddit '{subreddit_name}' not found in Database"}

        logger.info(f"Subreddit Metadata for '{subreddit_name}' successfully retrieved")
        return subreddit_metadata

    except Exception as e:
        logger.error(f"Error retrieving Metadata of Subreddit '{subreddit_name}'", exc_info=True)
        return {"error": f"Internal server error: {str(e)}"}


@app.get("/posts")
async def get_posts(subreddit_name: str, limit: int = 5) -> List[Dict[str, Any]]:
    """ Get Posts data with Sentiments endpoint """
    try:
        posts_data = retrieve_posts_data(subreddit_name, limit)

        if posts_data is None:
            logger.warning(f"No Posts Data for '{subreddit_name}' in DB found")
            return []

        logger.info(f"Posts data for Subreddit '{subreddit_name}' successfully retrieved")
        return posts_data

    except Exception as e:
        logger.error(f"Error retrieving Posts Data of Subreddit '{subreddit_name}': {e}", exc_info=True)
        return []


@app.get("/comments")
async def get_comments(subreddit_name: str, limit: int = 5) -> List[Dict[str, Any]]:
    """ Get Comments with Sentiments endpoint """
    try:
        comments_data = retrieve_comments_data(subreddit_name, limit)

        if comments_data is None:
            logger.warning(f"No Comments data for Subreddit '{subreddit_name}' found")
            return []

        logger.info(f"Comments data for Subreddit '{subreddit_name}' successfully retrieved")
        return comments_data

    except Exception as e:
        logger.error(f"Error retrieving Comments data of Subreddit '{subreddit_name}': {e}", exc_info=True)
        return []
