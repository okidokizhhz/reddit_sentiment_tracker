# ~/reddit_sentiment_tracker/src/storage/connection.py

import os
import subprocess
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import MetaData, text
from dotenv import load_dotenv
import logging

logger = logging.getLogger("reddit_sentiment_tracker")

# getting evironmental variables for db authentication
load_dotenv()
HOST_DB = os.getenv("HOST_DB")
NAME_DB = os.getenv("NAME_DB")
USER_DB = os.getenv("USER_DB")
PASSWORD_DB = os.getenv("PASSWORD_DB")
PORT_DB = os.getenv("PORT_DB")

# missing env var logic
required_vars = ["HOST_DB", "NAME_DB", "USER_DB", "PASSWORD_DB", "PORT_DB"]
missing_vars = []
for var in required_vars:
    if not os.getenv(var):
        missing_vars.append(var)

if missing_vars:
    logger.critical(f"DB: missing required variables: {', '.join(missing_vars)}")
    raise ValueError(f"DB: missing required variables: {', '.join(missing_vars)}")

# Setup, Connection to postgresql
try:
    engine = create_async_engine(f"postgresql+asyncpg://{USER_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}",
                           pool_size=5, 
                           max_overflow=10, 
                           pool_pre_ping=True)

    logger.info(f"Postgres Database created successfully")

except Exception as e:
    logger.critical(f"Error creating Postgres Database: {e}", exc_info=True)
    raise ValueError(f"Error creating Postgres Database: {e}")


# intitializing metadata object to hold table definitions
metadata = MetaData()


def run_alembic_migrations() -> bool:
    """ running Alembic migrations using subprocess command line call """
    try:
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            check=True
        )
        logger.info("Alembic migrations applied successfully")
        logger.debug(f"Alembic output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.critical(f"Alembic migrations failed: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        logger.critical(f"Failed to run Alembic: {e}")
        return False

# run migrations automatically when this module is imported
# run_alembic_migrations()


async def initialize_database() -> None:
    """ Test database connection - schema is managed by alembic """
    try:
        async with engine.begin() as conn:
            await conn.execute(text('SELECT 1'))         # text() tells sqlalchemy that raw SQL text should be executed
        logger.info("Database connection successful")
    except Exception as e:
        logger.critical(f"Error connecting to Database: {e}", exc_info=True)
        raise
