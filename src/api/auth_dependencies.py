# ~/reddit_sentiment_tracker/src/api/auth_dependencies.py

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .auth_service import verify_token

# Endpoint Protection logic
security = HTTPBearer()         # creating a "bearer token" checker

async def get_current_user(auth_data: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """ Checks if there is a valid JWT token 
        credentials as an object containing 1.scheme "Bearer" and 2.JWT token
        returns token user_id
    """

    token = auth_data.credentials    # assigning the actual JWT string to token

    payload = verify_token(token)     # decoding and verifying token

    if not payload:
        raise HTTPException(401, "Invalid token")

    return payload["user_id"]
