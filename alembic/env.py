from logging.config import fileConfig
from dotenv import load_dotenv
from sqlalchemy import create_engine
from alembic import context
import sys
import os

load_dotenv()

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.storage.schema_manager import metadata

# Get Alembic config
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use metadata
target_metadata = metadata

def get_database_url():
    """ Simple database URL for Docker """
    # Use environment variables with Docker defaults
    host = os.getenv("HOST_DB", "db")
    name = os.getenv("NAME_DB", "reddit_sentiment_tracker") 
    user = os.getenv("USER_DB", "postgres")
    password = os.getenv("PASSWORD_DB", "postgres")
    port = os.getenv("PORT_DB", "5432")
    
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"

def run_migrations_offline():
    """ Run migrations without database connection """
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """ Run migrations with database connection """
    engine = create_engine(get_database_url())
    
    with engine.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )
        
        with context.begin_transaction():
            context.run_migrations()

# Run the migration function
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
