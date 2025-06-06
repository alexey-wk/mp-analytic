from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_utilities import repeat_every
from app.service.rnp.rnp import rnp_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    @repeat_every(seconds=300)
    async def cron_job() -> None:
        await rnp_service.update_all_reports()
    
    await cron_job()
    yield