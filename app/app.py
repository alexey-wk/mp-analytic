import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controller.rnp import rnp_router
from app.controller.health import health_router
from app.controller.product_report import product_report_router
from app.controller.seller_account import seller_account_router
from app.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rnp_router)
app.include_router(product_report_router)
app.include_router(seller_account_router)
app.include_router(health_router)
