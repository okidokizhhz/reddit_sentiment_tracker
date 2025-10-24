# ~/reddit_sentiment_tracker/src/api/models.py

from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime


# /register
class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=40)    # ... = ellipsis; equal to Field(required=True)
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

# /subreddit_metadata/{subreddit_name}
class MetadataResponse(BaseModel):
    name: str = Field(..., description="Subreddit display name")
    description: Optional[str] = Field(None, description="Subreddit description")    # can be a str or None
    subscriber_count: Optional[int] = Field(None, description="Subreddit subscriber count")
    created_at: datetime = Field(..., description="Subreddit created at")

# /posts
class PostsResponse(BaseModel):
    id: str = Field(..., description="Post id")
    title: str = Field(..., description="Post title")
    author: str = Field(..., description="Post author")
    created_utc: datetime = Field(..., description="Post created at")
    title_sentiment: Dict[str, float] = Field(..., description="Post title sentiment")
    body_sentiment: Dict[str, float] = Field(..., description="Post body sentiment")
    score: int = Field(..., description="Post score")
    upvote_ratio: float = Field(..., description="Post upvote ratio")
    controversiality: float = Field(..., description="Post controversiality")
    num_comments: int = Field(..., description="Post number of comments")
    measured_at: datetime = Field(..., description="Post sentiment measured at")

# /comments
class CommentsResponse(BaseModel):
    id: str = Field(..., description="Comment id")
    author: str = Field(..., description="Comment author")
    text: str = Field(..., description="Comment text")
    score: int = Field(..., description="Comment score")
    created_utc: datetime = Field(..., description="Comment created at")
    comment_sentiment: Dict[str, float] = Field(..., description="Commment sentiment")
    measured_at: datetime = Field(..., description="Comment sentiment measured at")
