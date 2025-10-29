# ~/reddit_sentiment_tracker/src/api/rate_limiting.py

import logging
import redis.asyncio as redis
from fastapi import Depends, HTTPException
from typing import Any
from src.config import REDIS_URL, RATE_LIMIT_Redis, WINDOW_SIZE_Redis
from .auth_dependencies import get_current_user

logger = logging.getLogger("reddit_sentiment_tracker")

async def get_redis_client(REDIS_URL: str) -> Any:
    """ Getting Redis Client """
    try:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        await redis_client.ping()

        logger.info("Redis Client successfully retrieved")

        return redis_client

    except Exception as e:
        logger.error(f"Error initializing Redis Client: {e}", exc_info=True)
        raise


async def rate_limit_check(user_id: str = Depends(get_current_user)) -> str:
    """ Rate Limiting with redis. Check if user has exceeded the rate limit for api endpoints """

    redis_client = await get_redis_client(REDIS_URL)   # get Redis Client

    try:
        key = f"rate_limit:{user_id}"

        current = await redis_client(key)   # get current count - returns None if key doens't exist

        if current is None:
            current_count = 0
        else:
            current_count = int(current)

        if current_count >= RATE_LIMIT_Redis:         # check if limit is exceeded
            logger.warning(f"Rate limit exceeded for user {user_id}: {current_count}/{RATE_LIMIT_Redis}")
            raise HTTPException(status_code=429, detail=f"Rate limit exceeded for user {user_id}: {current_count}/{RATE_LIMIT_Redis}")

        async with redis_client.pipeline() as pipe:
            pipe.incr(key)
            pipe.expire(key, WINDOW_SIZE_Redis)
            await pipe.execute()

        logger.info(f"Rate Limit check passed for user {user_id}: {current_count + 1}/{RATE_LIMIT_Redis}")

        return user_id

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Rate Limit check failed: {e}", exc_info=True)
        return user_id
    finally:
        await redis_client.aclose()     # close redis connection
