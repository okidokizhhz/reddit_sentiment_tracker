# ~/reddit_sentiment_tracker/server.py

import sys
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from typing import Any, Dict, List, AsyncGenerator
from fastapi import FastAPI, HTTPException, Depends, Path, Query
from src.storage.schema_manager import users
from src.api.models import (RegisterRequest, RegisterResponse, 
                            LoginRequest, LoginResponse,
                            MetadataResponse, PostsResponse, CommentsResponse,
                            CollectionResponse)
from src.api.auth_service import create_access_token
from src.api.rate_limiting import rate_limit_check
from src.api.bcrypt_hashing import hash_password, verify_password
from src.api.password_validation import validate_password_strength
from src.storage.connection import initialize_database
from src.storage.crud import retrieve_metadata, retrieve_posts_data, retrieve_comments_data, db_session
from src.logger import setup_logger
from src.config import RATE_LIMIT_RISING_POSTS, RATE_LIMIT_TOP_POSTS, COMMENT_LIMIT, TOP_POSTS_TIME_FILTER, REPLY_DEPTH
from src.data_pipeline_orchestrator import (reddit_client, get_subreddit_metadata,
                                         subreddit_data_into_db, get_top_posts, top_posts_data_into_db,
                                         comments_top_posts_into_db, get_rising_posts, rising_posts_data_into_db,
                                         comments_rising_posts_into_db)

logger = setup_logger("reddit_sentiment_tracker")


# lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """ handle startup, db initialization, shutdown """
    logger.info("Reddit Sentiment Tracker API starting up...")     # startup

    try:
        await initialize_database()
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


@app.get(
    "/health",
    tags=["monitoring"],
    summary="API Health Check",
    description="Check if the API service is running correctly and get basic service information"
)                                               # get request to /health
async def health_check() -> dict[str, Any]:
    """ Health check endpoint for monitoring the API """
    return {
        "status": "healthy",
        "service": "Reddit Sentiment Tracker API",
        "timestamp": datetime.now(timezone.utc),
        "message": "API is running correctly",
        "environment": "development"
    }


@app.post(
    "/collect/{subreddit_name}",
    dependencies=[Depends(rate_limit_check)],
    response_model=CollectionResponse,
    tags=["collection"],
    summary="Subreddit Data Collection",
    description="Collect datasets about a subreddit: metadata, posts, comments, sentiments that can be retrieved through get endpoints"
)
async def collect_data(
    subreddit_name: str = Path(..., min_length=2, max_length=21, description="Subreddit name (2-21 characters)"),
    user_id: str = Depends(rate_limit_check)
) -> CollectionResponse:
    """ Enduser can type in a subreddit name to fetch various datasets which then get stored in the database """
    subreddit_name = subreddit_name.lower()

    try:
        # Getting Reddit Client
        reddit = await reddit_client()
        if not reddit:
            logger.error(f"Failed to retrieve reddit client")
            raise ValueError(f"Failed to retrieve reddit client")

        # Metadata subreddit fetching
        subreddit_metadata, subreddit_id = await get_subreddit_metadata(subreddit_name, reddit)
        if not subreddit_metadata or "id" not in subreddit_metadata:
            logger.error(f"Failed to fetch data for subreddit: '{subreddit_name}'")
            raise ValueError(f"Failed to fetch data for subreddit: '{subreddit_name}'")

        # DB: inserting Metadata
        await subreddit_data_into_db(subreddit_name, subreddit_metadata)

        # Top Posts fetching
        top_posts_data = await get_top_posts(
            subreddit_name,
            reddit,
            RATE_LIMIT_TOP_POSTS,
            TOP_POSTS_TIME_FILTER
        )
        if not top_posts_data:
            logger.error(f"Failed to fetch top posts - skipping insertion of top posts data and top posts sentiment into DB")
        else:
            # Inserting Top Posts into DB (with Sentiment)
            await top_posts_data_into_db(top_posts_data, subreddit_id)
            # Commments (top posts) fetching + Inserting into DB
            await comments_top_posts_into_db(
                top_posts_data,
                reddit,
                REPLY_DEPTH,
                COMMENT_LIMIT
            )

        # Rising Posts fetching
        rising_posts_data = await get_rising_posts(
            subreddit_name,
            reddit,
            RATE_LIMIT_RISING_POSTS
        )
        if not rising_posts_data:
            logger.error(f"Failed to fetch rising posts skipping insertion of rising posts data and rising posts sentiment into DB")
        else:
            # Inserting Rising Posts into DB (with Sentiment)
            await rising_posts_data_into_db(rising_posts_data, subreddit_id)
            # Rising Posts Comments fetching + Inserting into Db (with Sentiment)
            await comments_rising_posts_into_db(
                rising_posts_data,
                reddit,
                REPLY_DEPTH,
                COMMENT_LIMIT
            )

        return CollectionResponse(
            status="success",
            message=f"Data collection finished fully/partially for subreddit /{subreddit_name}",
            subreddit_name=f"{subreddit_name}"
        )

    except HTTPException:
        raise
    except (ValueError, Exception) as e:
        logger.error(f"Data Collection: Pipeline failed for subreddit '{subreddit_name}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during Collection of Data")
    finally:
        if reddit:
            await reddit.close()


@app.get(
    "/subreddit_metadata/{subreddit_name}", 
    dependencies=[Depends(rate_limit_check)],
    response_model=MetadataResponse,
    tags=["subreddits"],
    summary="Get Subreddit Metadata",
    description="Retrieve comprehensive Metadata for a specific Subreddit such as the description, subscriber count, date of creation"
)
async def get_subreddit_metadata(
    subreddit_name: str = Path(..., min_length=2, max_length=21, description="Subreddit name (2-21 characters)"),
    user_id: str = Depends(rate_limit_check)
) -> MetadataResponse:
    """ Get Subreddit Metadata (name, description, subscriber count, created at) endpoint """
    subreddit_name = subreddit_name.lower()

    try:
        subreddit_metadata = await retrieve_metadata(subreddit_name)

        if subreddit_metadata is None:
            logger.warning(f"No data for '{subreddit_name}' in DB found")
            raise HTTPException(status_code=404, detail=f"No database entry for Metadata of subreddit: '{subreddit_name}'")

        logger.info(f"Subreddit Metadata for '{subreddit_name}' successfully retrieved")

        return MetadataResponse(
            status="success",
            **subreddit_metadata    # ** dictionary unpacking / kwargs unpacking
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving Metadata of Subreddit '{subreddit_name}'", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get(
    "/posts/{subreddit_name}", 
    dependencies=[Depends(rate_limit_check)],
    response_model=List[PostsResponse],
    tags=["posts"],
    summary="Get Posts Data with corresponding Sentiments",
    description="Retrieve comprehensive data for Posts of a specific Subreddit such as author, title, upvote ratio, number of comments, post sentiment, controversiality"
)
async def get_posts(
    subreddit_name: str = Path(..., min_length=2, max_length=21, description="Subreddit name (2-21 characters)"),
    limit: int = Query(5, ge=1, le=100),
    user_id: str = Depends(rate_limit_check)
) -> List[Dict[str, Any]]:
    """ Get Posts data with Sentiments endpoint """
    subreddit_name = subreddit_name.lower()

    try:
        posts_data = await retrieve_posts_data(subreddit_name, limit)

        if posts_data is None:
            logger.warning(f"No Posts Data for '{subreddit_name}' in DB found")
            raise HTTPException(status_code=404, detail=f"No database entry for posts of subreddit: '{subreddit_name}' found")

        logger.info(f"Posts data for Subreddit '{subreddit_name}' successfully retrieved")
        return posts_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving Posts Data of Subreddit '{subreddit_name}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get(
    "/comments/{subreddit_name}", 
    dependencies=[Depends(rate_limit_check)],
    response_model=List[CommentsResponse],
    tags=["comments"],
    summary="Get Comments data with corresponding Sentiments",
    description="Retrieve comprehensive data for Comments of a specific Post from a specific Subreddit such as author, comment sentiment, comment score, date of creation"
)
async def get_comments(
    subreddit_name: str = Path(..., min_length=2, max_length=21, description="Subreddit name (2-21 characters)"),
    limit: int = Query(5, ge=1, le=100),
    user_id: str= Depends(rate_limit_check)
) -> List[Dict[str, Any]]:
    """ Get Comments with Sentiments endpoint """
    subreddit_name = subreddit_name.lower()

    try:
        comments_data = await retrieve_comments_data(subreddit_name, limit)

        if comments_data is None:
            logger.warning(f"No Comments data for Subreddit '{subreddit_name}' found")
            raise HTTPException(status_code=404, detail=f"No database entry for comments of subreddit: '{subreddit_name}' found")

        logger.info(f"Comments data for Subreddit '{subreddit_name}' successfully retrieved")
        return comments_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving Comments data of Subreddit '{subreddit_name}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post(
    "/register", 
    response_model=RegisterResponse,
    tags=["authentication"],
    summary="Register new user"
)
async def register(request: RegisterRequest) -> RegisterResponse:
    """ Enduser can register using username, email, password """
    try:
        async with db_session() as conn:
            # checking if username already exists
            existing_user = (await conn.execute(
                users.select().where(users.c.username == request.username)
            )).first()
            if existing_user:
                logger.warning(f"Registration failed: Username '{request.username}' already exists")
                raise HTTPException(status_code=400, detail="Username already exists")

            # checking if email already exists
            existing_email = (await conn.execute(
                users.select().where(users.c.email == request.email)
            )).first()
            if existing_email:
                logger.warning(f"Registration failed: Email '{request.email}' already exists")
                raise HTTPException(status_code=400, detail="Email already exists")

            # password strength validation
            validate_password_strength(request.password)

            # hashing request.password with bcrypt
            hashed_pw = hash_password(request.password)

            # User Creation (if there are no duplicates) + DB insertion
            await conn.execute(users.insert().values(
                username=request.username,
                email=request.email,
                hashed_password=hashed_pw
            ))

            logger.info(f"User '{request.username}' with email '{request.email}' successfully created.")

            return RegisterResponse(status="success")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))



@app.post(
    "/login", 
    response_model=LoginResponse,
    tags=["authentication"],
    summary="User Login"
)
async def login(request: LoginRequest) -> LoginResponse:
    """ Login Endpoint for enduser """
    try:
        async with db_session() as conn:
            # checking if username exists in Db
            existing_user = (await conn.execute(
                users.select().where(users.c.username == request.username)
            )).first()

            # throw Error if username does not exist
            if not existing_user:
                logger.warning(f"Login failed: Username '{request.username}' does not exist")
                raise HTTPException(status_code=400, detail="Username does not exists")

            # extract hashed_password from existing user result
            hashed_password = existing_user.hashed_password

            # verifying hashed_password
            if verify_password(request.password, hashed_password):
                logger.info("The password is correct")

                # creating JWT Token with data
                data = {"sub": existing_user.username, "user_id": existing_user.id}
                jwt_token = create_access_token(data=data, expires_delta=None)

                return LoginResponse(
                    status="success",
                    access_token=jwt_token,
                    token_type="bearer"
                )

            else:
                logger.warning(f"Invalid password for user: '{request.username}'. Login failed")
                raise HTTPException(status_code=400, detail="Invalid password")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during login")
