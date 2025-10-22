# ~/reddit_sentiment_tracker/src/api/auth_service.py

import os
import jwt
import logging
from typing import Optional
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

logger = logging.getLogger("reddit_sentiment_tracker")

load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("JWT_KEY")
ALGORITHM = "HS256"                     # encryption algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 30        # token validity period


def check_secret_key_existence() -> str:
    """ Checks if SECRET_KEY is existent """
    if SECRET_KEY is not None:
        return SECRET_KEY
    else:
        logger.critical(f"No Secret Key found in environmental variables")
        raise ValueError("SECRET_KEY variable is required")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """ Creating new JWT access token """
    SECRET_KEY = check_secret_key_existence()

    try:
        # creating a copy of the data - avoid modifying original data
        to_encode = data.copy()

        # calculating token expiration time
        if expires_delta:   # custom expiration time
            expire = datetime.now(timezone.utc) + expires_delta
        else:   # default expiration time
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        # adding expiration claim to the token data - dictionary with the key "exp" in standard for JWT
        to_encode.update({"exp": expire})

        # Encoding the JWT token
        # jwt.encode() creates the token with:
        # - payload (to_encode): the data we want to store
        # - secret key (SECRET_KEY): used to sign the token
        # - algorithm (ALGORITHM): how to encrypt/sign the token
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        logger.info(f"JWT token created successfully. Expires at: {expire}")

        return encoded_jwt      # returning encoded JWT token

    except Exception as e:
        logger.error(f"JWT token creation failed: {e}", exc_info=True)
        raise


def verify_token(token: str) -> Optional[dict]:
    """ Verifies JWT token and returns the payload if valid """
    SECRET_KEY = check_secret_key_existence()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        logger.info("JWT token verified")

        return payload

    except jwt.ExpiredSignatureError:
        logger.error(f"JWT token is Invalid. Expired Signature Error")
        return None     # token is expired
    except jwt.InvalidTokenError:
        logger.error(f"JWT token is Invalid. Invalid Token Error")
        return None     # token is invalid
