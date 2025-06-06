from sqlalchemy.orm import Session
from app.repository.entity.seller_account import SellerAccount

def create_seller_account(db: Session, name: str, api_token: str, auth_cookies: str):
    entity = SellerAccount(name=name, api_token=api_token, auth_cookies=auth_cookies)
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity.id

def get_all_seller_accounts(db: Session) -> list[SellerAccount]:
    return db.query(SellerAccount).all()

def get_seller_account_by_id(db: Session, id: int) -> SellerAccount:
    return db.query(SellerAccount).filter(SellerAccount.id == id).first()

def get_seller_account_by_name(db: Session, name: str) -> SellerAccount:
    return db.query(SellerAccount).filter(SellerAccount.name == name).first()

def update_seller_account(db: Session, id: int, name: str, api_token: str, auth_cookies: str) -> SellerAccount:
    entity = get_seller_account_by_id(db, id)
    if entity:
        entity.name = name
        entity.api_token = api_token
        entity.auth_cookies = auth_cookies
        db.commit()
        db.refresh(entity)
    return entity

def delete_seller_account(db: Session, id: int) -> bool:
    entity = get_seller_account_by_id(db, id)
    if entity:
        db.delete(entity)
        db.commit()
        return True
    return False
