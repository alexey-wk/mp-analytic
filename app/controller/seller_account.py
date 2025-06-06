from fastapi import APIRouter
from app.service.seller_account.seller_account import seller_account_service
from app.controller.request.seller_account import CreateSellerAccountRequest, UpdateSellerAccountRequest

seller_account_router = APIRouter()

@seller_account_router.post("/seller-account/create")
async def create_seller_account(req: CreateSellerAccountRequest):
    seller_account_id = seller_account_service.create_seller_account(req)
    return {"seller_account_id": seller_account_id}

@seller_account_router.post("/seller-account/update")
async def update_seller_account(req: UpdateSellerAccountRequest):
    updated_seller_account = seller_account_service.update_seller_account(req)
    return updated_seller_account
