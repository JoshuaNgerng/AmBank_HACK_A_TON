from typing import Dict, Any, Optional
from functools import lru_cache
from celery import Celery

from app.core.config import settings
from app.core.logging import logger

# Global Celery app instance
celery_app: Optional[Celery] = None

def get_celery_config() -> Dict[str, Any]:
    """
    Get Celery configuration options based on application settings.
    
    Returns:
        Dictionary of Celery configuration options
    """
    if not settings.CELERY_ENABLED:
        return {}
        
    if not settings.REDIS_ENABLED:
        logger.warning(
            "Celery is enabled but Redis is disabled. "
            "Redis is required for Celery. "
            "Please enable Redis or disable Celery."
        )
        return {}
    
    # Build broker URL from Redis settings
    broker_url = settings.REDIS_URL
    
    # Set up result backend - also using Redis
    result_backend = settings.REDIS_URL
    
    # Configure Celery
    config = {
        "broker_url": broker_url,
        "result_backend": result_backend,
        "broker_connection_retry_on_startup": True,
        "task_serializer": "json",
        "accept_content": ["json"],
        "result_serializer": "json",
        "enable_utc": True,
        "task_track_started": True,
        "task_time_limit": 30 * 60,  # 30 minutes
        "worker_max_tasks_per_child": 1000,
        "task_default_queue": "celery",
        "worker_prefetch_multiplier": 2, # lower it so dont load too much memory in advance
    }
    
    # Add Redis password if configured
    if settings.REDIS_PASSWORD:
        if "redis://" in broker_url:
            # If using Redis protocol, update the URLs with password
            password_part = f":{settings.REDIS_PASSWORD}@"
            if "@" in broker_url:
                # Replace existing auth info
                config["broker_url"] = broker_url.replace("@", password_part)
                config["result_backend"] = result_backend.replace("@", password_part)
            else:
                # Add auth info after protocol and before host
                parts = broker_url.split("://")
                if len(parts) == 2:
                    config["broker_url"] = f"{parts[0]}://{password_part}{parts[1]}"
                    config["result_backend"] = f"{parts[0]}://{password_part}{parts[1]}"
    
    return config


@lru_cache()
def create_celery_app() -> Optional[Celery]:
    """
    Create and configure the Celery application.
    Returns None if Celery is disabled in settings.
    
    Returns:
        Configured Celery application instance or None
    """
    global celery_app
    
    if not settings.CELERY_ENABLED:
        logger.info("Celery is disabled in configuration")
        return None
        
    if not settings.REDIS_ENABLED:
        logger.warning(
            "Cannot create Celery app: Redis is disabled but required for Celery. "
            "Please enable Redis or disable Celery."
        )
        return None
    
    try:
        config = get_celery_config()
        if not config:
            return None
            
        # Create Celery app
        celery_instance = Celery(settings.APP_NAME)
        
        # Update configuration
        celery_instance.conf.update(config)
        
        # Auto-discover tasks
        celery_instance.autodiscover_tasks(
            ["app.ocr"], 
            related_name=None, # type: ignore
            force=True
        )
        
        celery_app = celery_instance
        
        logger.info("Celery application initialized successfully")
        return celery_instance
    except Exception as e:
        logger.error(f"Failed to initialize Celery: {str(e)}")
        return None


def get_celery_app() -> Optional[Celery]:
    """
    Get the Celery application instance.
    Creates the instance if it doesn't exist yet.
    
    Returns:
        Celery application instance or None if Celery is disabled
    """
    global celery_app
    
    if not settings.CELERY_ENABLED:
        return None
        
    if celery_app is None:
        celery_app = create_celery_app()
        
    return celery_app 

get_celery_app()
