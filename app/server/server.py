import uvicorn
from fastapi import FastAPI, APIRouter, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from app.handler import Handler
from app.server.model import FillRangeRequest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@router.post("/rnp/fill-range")
async def fill_range(req: FillRangeRequest, background_tasks: BackgroundTasks):
    handler = Handler()
    
    background_tasks.add_task(
        handler.fill_range,
        req.dateFrom, 
        req.dateTo, 
        req.apiToken, 
        req.authCookies, 
        req.googleSheetsCreds, 
        req.spreadsheetName, 
        req.worksheetNames
    )
    
    return {"message": "Job started in background"}

app.include_router(router)

def run_server():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )