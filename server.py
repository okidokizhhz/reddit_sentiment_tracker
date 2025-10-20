# ~/reddit_sentiment_tracker/server.py

import sys
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.logger import setup_logger
from src.storage.connection import initialize_database

logger = setup_logger("reddit_sentiment_tracker")

# lifespan context manager
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


@app.get("/")
async def read_root():
    """ root """
    return {"message": "welcome to", "program": "reddit sentiment tracker"}


@app.get("/health")                                               # get request to /health path
async def health_check():
    """ Health check endpoint for monitoring the API """
    return {
        "status": "healthy",
        "service": "Reddit Sentiment Tracker API",
        "timestamp": datetime.now(timezone.utc),
        "message": "API is running correctly",
        "environment": "development"
    }
