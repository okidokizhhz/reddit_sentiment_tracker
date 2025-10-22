# ~/reddit_sentiment_tracker/tests/conftest.py
# Setting upo the configuration for test Database "test_reddit_sentiment_tracker" using already existing schema

import os
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from src.storage.connection import metadata

# Fixtures:
    # eliminate boilerplate (no repeating setup code)
    # prevent resource leaks (automatic cleanup)
    # make tests faster (smart resource reuse)
    # make tests more reliable (cleanup always happens)
    # make tests easier to write (focus on test logic)

load_dotenv()
# fixture = creates engine once for ALL tests - engine gets reused for every test - fast and efficient
# scope "session" = expensive logic (in this case: engine) created once
@pytest.fixture(scope="session")
def test_engine():
    """ Creating a test database engine with the scope "session" to reuse the connection """
    HOST_DB = os.getenv("HOST_DB")
    NAME_DB = "test_reddit_sentiment_tracker"   # using test db
    USER_DB = os.getenv("USER_DB")
    PASSWORD_DB = os.getenv("PASSWORD_DB")
    PORT_DB = os.getenv("PORT_DB")

    # Setup, Connection to test db postgresql
    try:
        test_engine = create_engine(f"postgresql://{USER_DB}:{PASSWORD_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}",
                               pool_size=5, 
                               max_overflow=10, 
                               pool_pre_ping=True)
        return test_engine

    except Exception as e:
        raise pytest.fail(f"Error creating test Postgres Database: {e}")

# fixture = 
# scope "function" = fresh instance created for EVERY test function - each test needs isolated database state (transaction rollback)
@pytest.fixture(scope="function")
def db_session(test_engine):   # reuses the same test_engine for every test performed - fast and efficient
    """ Creating a fresh database session for each test with transaction rollback """
    connection = test_engine.connect()      # connecting to engine
    transaction = connection.begin()   # beginning transaction

    try:
        metadata.create_all(connection)     # creating all tables for this test session
        yield connection
    finally:
        transaction.rollback()  # rolling back the transaction
        connection.close()      # closing the test db connection
