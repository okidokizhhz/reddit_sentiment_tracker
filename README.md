```markdown
# Reddit Sentiment Tracker

A FastAPI-based web application that tracks and analyzes sentiment from Reddit posts and comments in real-time. This project demonstrates backend development skills with Python, FastAPI, PostgreSQL.

## Features

- Real-time Reddit data collection using AsyncPRAW
- Sentiment analysis using VADER sentiment analysis
- PostgreSQL database for data storage
- Redis for rate limiting
- FastAPI RESTful API with automatic documentation
- JWT authentication system
- Docker containerization

## Tech Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Rate Limiting**: Redis
- **Authentication**: JWT tokens
- **Containerization**: Docker
- **Migrations**: Alembic
- **Testing**: Pytest

## API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login with JWT token

### Data Access (Requires Authentication)
- `GET /subreddit_metadata/{subreddit_name}` - Get subreddit information
- `GET /posts/{subreddit_name}` - Get posts with sentiment analysis
- `GET /comments/{subreddit_name}` - Get comments with sentiment analysis

### Monitoring
- `GET /health` - API health check

## Installation & Setup

### Prerequisites
- Python 3.11+
- PostgreSQL
- Redis
- Reddit API credentials

### Local Development
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (see Configuration section)
4. Run database migrations: `alembic upgrade head`
5. Start the application: `uvicorn server:app --reload`

### Docker Deployment
```bash
docker-compose up --build
```

## Configuration

Required environment variables:

```bash
# Reddit API
CLIENT_ID=your_reddit_client_id
SECRET_KEY=your_reddit_secret_key
USER_AGENT=your_user_agent
REDDIT_USERNAME=your_reddit_username
REDDIT_PW=your_reddit_password

# Database
HOST_DB=your_database_host
NAME_DB=your_database_name
USER_DB=your_database_user
PASSWORD_DB=your_database_password
PORT_DB=5432

# Redis
REDIS_URL=your_redis_url

# JWT
JWT_KEY=your_jwt_secret_key
JWT_ALGORITHM=HS256
```

## Development Features

- Logging
- Error handling and validation
- Type hints throughout
- Unit tests with pytest
- Database migrations with Alembic
- Rate limiting to prevent API abuse
- Password strength validation

## Deployment

The application is containerized with Docker and can be deployed to any container platform. The current deployment uses Koyeb with:

- Automatic builds from GitHub
- Environment-based configuration
- Health checks and monitoring

## Skills Demonstrated

This project showcases:
- FastAPI development with async/await
- PostgreSQL database design and management
- JWT authentication implementation
- Docker containerization
- API rate limiting and security
- Environment-based configuration

## License

MIT License
```

This README is professional, clean, and highlights the technical skills that would be relevant for a junior Python backend developer position in Vienna. It focuses on the technologies used, architecture decisions, and demonstrates your understanding of modern backend development practices.
