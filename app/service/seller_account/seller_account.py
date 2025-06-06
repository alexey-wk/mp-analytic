from app.controller.request.seller_account import CreateSellerAccountRequest, UpdateSellerAccountRequest
from app.repository.seller_account import create_seller_account, update_seller_account, get_all_seller_accounts
from app.repository.db import get_db
class SellerAccountService:
    def create_seller_account(self, req: CreateSellerAccountRequest):
        db = next(get_db())
        return create_seller_account(
            db,
            req.name,
            req.apiToken,
            req.authCookies
        )

    def update_seller_account(self, req: UpdateSellerAccountRequest):
        db = next(get_db())
        return update_seller_account(
            db,
            req.id,
            req.name,
            req.apiToken,
            req.authCookies
        )
    
    def get_all_seller_accounts(self):
        db = next(get_db())
        return get_all_seller_accounts(db)
    
seller_account_service = SellerAccountService()