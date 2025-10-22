# ~/reddit_sentiment_tracker/src/api/models.py

from pydantic import BaseModel, Field


# /register
class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=40)
    email: str = Field(..., min_length=5, max_length=40)
    password: str = Field(..., min_length=5, max_length=40)

class RegisterResponse(BaseModel):
    status: str

# /login
class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=40)
    password: str = Field(..., min_length=5, max_length=40)

class LoginResponse(BaseModel):
    status: str
    access_token: str
    token_type: str = "bearer"
