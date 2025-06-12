from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.service.rnp.rnp import rnp_service
from app.repository.db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    scheduler = AsyncIOScheduler()
    
    async def cron_job() -> None:
        await rnp_service.update_all_reports()
    
    scheduler.add_job(cron_job, CronTrigger.from_crontab('0 0 * * *'))
    
    scheduler.start()
    yield
    scheduler.shutdown()