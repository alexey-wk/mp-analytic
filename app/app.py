import uvicorn
from fastapi import FastAPI
from app.repository.db import init_db
from app.controller.rnp import rnp_router
from app.controller.product_report import product_report_router
from app.controller.seller_account import seller_account_router
from app.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(rnp_router)
app.include_router(product_report_router)
app.include_router(seller_account_router)

def run_server():
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)