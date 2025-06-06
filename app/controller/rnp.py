from fastapi import APIRouter, BackgroundTasks
from app.service.rnp.rnp import rnp_service
from app.controller.request.rnp import FillRangeRequest

rnp_router = APIRouter()

@rnp_router.post("/rnp/fill-range")
async def fill_range(req: FillRangeRequest, background_tasks: BackgroundTasks):    
    background_tasks.add_task(
        rnp_service.fill_range_by_req,
        req.dateFrom, 
        req.dateTo, 
        req.apiToken, 
        req.authCookies, 
        req.spreadsheetName, 
        req.worksheetNames
    )
    
    return {"message": "Job started in background"}
