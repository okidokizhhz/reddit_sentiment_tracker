---
title: Reddit Sentiment Tracker
emoji: 🔍
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# Reddit Sentiment Tracker

Track sentiment analysis for Reddit posts and comments in real-time.

## Features

- Real-time Reddit data collection
- Sentiment analysis using VADER
- PostgreSQL database storage
- Redis caching and rate limiting
- FastAPI RESTful API
- JWT authentication

## API Endpoints

- `GET /health` - Health check
- `GET /subreddit_metadata/{subreddit_name}` - Get subreddit info
- `GET /posts/{subreddit_name}` - Get posts with sentiment
- `GET /comments/{subreddit_name}` - Get comments with sentiment
- `POST /register` - User registration
- `POST /login` - User login
