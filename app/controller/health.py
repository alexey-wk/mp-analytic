import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)
health_router = APIRouter()

@health_router.get("/health")
async def health():
    logger.info("Health check")
    return {}
