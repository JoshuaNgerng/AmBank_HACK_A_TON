from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.logging import setup_logging, logger
from endpoints.router import api_router


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """
#     Lifespan context manager for FastAPI application.
#     Handles startup and shutdown events.
#     """
#     # Startup operations
#     logger.info(f"Starting up {settings.APP_NAME}")
    
#     # Initialize Redis if enabled
#     redis_ok = False
#     if settings.REDIS_ENABLED:
#         # Initialize Redis pool
#         redis_pool = await get_redis_pool()
#         if redis_pool:
#             logger.info("Redis connection pool initialized")
            
#             # Check if Redis server is actually reachable
#             redis_ok = await check_redis_connection()
#             if not redis_ok:
#                 logger.warning(
#                     "Redis is enabled but server is not reachable. "
#                     "Please check Redis server status and connection settings. "
#                     "Application will continue running but Redis features will not work."
#                 )
#         else:
#             logger.warning("Failed to initialize Redis connection pool")
    
#     # Initialize Celery if enabled and Redis is available
#     if settings.CELERY_ENABLED:
#         if not settings.REDIS_ENABLED or not redis_ok:
#             logger.warning(
#                 "Celery is enabled but Redis is not available. "
#                 "Celery requires Redis to function. "
#                 "Celery features will not work until Redis is available."
#             )
#         else:
#             # Initialize Celery app
#             celery_app = create_celery_app()
#             if celery_app:
#                 logger.info("Celery application initialized successfully")
#             else:
#                 logger.warning("Failed to initialize Celery application")
    
#     logger.info("Application initialization completed successfully")
    
#     yield
    
#     # Shutdown operations
    
#     if settings.REDIS_ENABLED:
#         await close_redis_pool()
        
#     logger.info(f"Shutting down {settings.APP_NAME}")


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    # Initialize logging
    app_logger = setup_logging()
    
    app = FastAPI(
        title=settings.APP_NAME,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url=f"{settings.API_PREFIX}/docs",
        redoc_url=f"{settings.API_PREFIX}/redoc",
        # lifespan=lifespan,
    )
    
    # # Add middlewares - order matters!
    
    # # Error handler should be first to catch all exceptions
    # app.add_middleware(ErrorHandlerMiddleware)
    
    # # Protect documentation with authentication
    # app.add_middleware(DocsSecurityMiddleware)
    
    # # Logging middleware
    # app.add_middleware(LoggingMiddleware)
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Modify in production to specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    app.include_router(api_router, prefix=settings.API_PREFIX)

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        app_logger.info("Health check endpoint called")
        return {"status": "healthy"}
    # make sure paddleocr fetch all the models from remote 
    return app


app = create_application()

# Log application startup
logger.info(f"{settings.APP_NAME} initialized and ready")
