# ~/reddit_sentiment_tracker/server.py

import sys
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from typing import Any, Dict, List, AsyncGenerator
from fastapi import FastAPI, HTTPException, Depends, Path
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.storage.schema_manager import users
from src.api.models import (RegisterRequest, RegisterResponse, 
                            LoginRequest, LoginResponse,
                            MetadataResponse,
                            PostsResponse,
                            CommentsResponse)
from src.api.auth_service import create_access_token, verify_token
from src.api.bcrypt_hashing import hash_password, verify_password
from src.api.password_validation import validate_password_strength
from src.storage.connection import initialize_database
from src.storage.crud import retrieve_metadata, retrieve_posts_data, retrieve_comments_data, db_session
from src.logger import setup_logger

logger = setup_logger("reddit_sentiment_tracker")


# Endpoint Protection logic
security = HTTPBearer() # creating a "bearer token" checker
async def get_current_user(auth_data: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """ Checks if there is a valid JWT token 
        credentials as an object containing 1.scheme "Bearer" and 2.JWT token
    """
    token = auth_data.credentials    # assigning the actual JWT string to token
    payload = verify_token(token)     # decoding and verifying token
    if not payload:
        raise HTTPException(401, "Invalid token")
    return payload["user_id"]


# lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
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


@app.get("/health")                                               # get request to /health
async def health_check() -> dict[str, Any]:
    """ Health check endpoint for monitoring the API """
    return {
        "status": "healthy",
        "service": "Reddit Sentiment Tracker API",
        "timestamp": datetime.now(timezone.utc),
        "message": "API is running correctly",
        "environment": "development"
    }


@app.get("/subreddit_metadata/{subreddit_name}", response_model=MetadataResponse)       # get request to /subreddit_metadata with parameter
async def get_subreddit_metadata(
    subreddit_name: str = Path(..., min_length=2, max_length=21, description="Subreddit name (2-21 characters)")
) -> MetadataResponse:
    """ Get Subreddit Metadata (name, description, subscriber count, created at) endpoint """
    subreddit_name = subreddit_name.lower()

    try:
        subreddit_metadata = retrieve_metadata(subreddit_name)

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


@app.get("/posts/{subreddit_name}", response_model=List[PostsResponse])
async def get_posts(
    subreddit_name: str = Path(..., min_length=2, max_length=21, description="Subreddit name (2-21 characters)"),
    limit: int = 5, 
    user_id: str= Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """ Get Posts data with Sentiments endpoint """
    subreddit_name = subreddit_name.lower()

    try:
        posts_data = retrieve_posts_data(subreddit_name, limit)

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


@app.get("/comments/{subreddit_name}", response_model=List[CommentsResponse])
async def get_comments(
    subreddit_name: str = Path(..., min_length=2, max_length=21, description="Subreddit name (2-21 characters)"),
    limit: int = 5, 
    user_id: str= Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """ Get Comments with Sentiments endpoint """
    subreddit_name = subreddit_name.lower()

    try:
        comments_data = retrieve_comments_data(subreddit_name, limit)

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

@app.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest) -> RegisterResponse:
    """ Enduser can register using username, email, password """
    try:
        with db_session() as conn:
            # checking if username already exists
            existing_user = conn.execute(
                users.select().where(users.c.username == request.username)
            ).first()
            if existing_user:
                logger.warning(f"Registration failed: Username '{request.username}' already exists")
                raise HTTPException(status_code=400, detail="Username already exists")

            # checking if email already exists
            existing_email = conn.execute(
                users.select().where(users.c.email == request.email)
            ).first()
            if existing_email:
                logger.warning(f"Registration failed: Email '{request.email}' already exists")
                raise HTTPException(status_code=400, detail="Email already exists")

            # password strength validation
            validate_password_strength(request.password)

            # hashing request.password with bcrypt
            hashed_pw = hash_password(request.password)

            # User Creation (if there are no duplicates) + DB insertion
            conn.execute(users.insert().values(
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


@app.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest) -> LoginResponse:
    """ Login Endpoint for enduser """
    try:
        with db_session() as conn:
            # checking if username exists in Db
            existing_user = conn.execute(
                users.select().where(users.c.username == request.username)
            ).first()

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
