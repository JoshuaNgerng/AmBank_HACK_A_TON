import traceback
from typing import Optional
import redis.asyncio as redis
from redis.asyncio import Redis, ConnectionPool

from app.core.config import settings
from app.core.logging import logger

# Global Redis connection pool
redis_pool: Optional[ConnectionPool] = None


async def get_redis_pool() -> Optional[ConnectionPool]:
    """
    Get or create a Redis connection pool.
    Returns None if Redis is disabled.
    """
    global redis_pool
    
    if not settings.REDIS_ENABLED:
        return None
        
    if redis_pool is None:
        try:
            redis_kwargs = {
                "decode_responses": True,
                "encoding": "utf-8",
                "max_connections": settings.REDIS_POOL_SIZE,
                "socket_timeout": settings.REDIS_TIMEOUT,
                "socket_connect_timeout": settings.REDIS_TIMEOUT,
            }
            
            if settings.REDIS_PASSWORD:
                redis_kwargs["password"] = settings.REDIS_PASSWORD
                
            redis_pool = ConnectionPool.from_url(
                settings.REDIS_URL,
                **redis_kwargs
            )
            logger.info("Redis connection pool created")
        except Exception as e:
            logger.error(f"Failed to create Redis connection pool: {str(e)}")
            return None
            
    return redis_pool


async def get_redis() -> Optional[Redis]:
    """
    Get a Redis client from the connection pool.
    Returns None if Redis is disabled.
    """
    if not settings.REDIS_ENABLED:
        return None
        
    pool = await get_redis_pool()
    if pool is None:
        return None
        
    try:
        return redis.Redis(connection_pool=pool)
    except Exception as e:
        logger.error(f"Failed to get Redis client: {str(e)}")
        return None


async def close_redis_pool() -> None:
    """Close the Redis connection pool if it exists."""
    global redis_pool
    
    if redis_pool is not None:
        try:
            await redis_pool.disconnect()
            redis_pool = None
            logger.info("Redis connection pool closed")
        except Exception as e:
            logger.error(f"Error closing Redis connection pool: {str(e)}")

async def check_redis_connection() -> bool:
    """
    Check if Redis connection can be established.
    Returns True if connection successful, False otherwise.
    """
    if not settings.REDIS_ENABLED:
        logger.info("Redis is disabled, skipping connection check")
        return False
    redis_client = None 
    try:
        redis_client = await get_redis()
        if redis_client is None:
            logger.error("Failed to get Redis client for connection check")
            return False
            
        # Try a simple PING command to verify connection
        result = await redis_client.ping()
        if result:
            logger.info("Redis connection check succeeded: Redis server is reachable")
            return True
        else:
            logger.error("Redis connection check failed: No response from Redis server")
            return False
    except Exception as e:
        logger.error(f"Redis connection check failed: {str(e)}")
        logger.debug(traceback.format_exc())
        return False
    finally:
        if redis_client:
            await redis_client.close()