from sqlalchemy.orm import Session
from app.repository.entity.product_report import ProductReport

def create_product_report(db: Session, seller_account_id: int, spreadsheet_name: str, worksheet_name: str):
    entity = ProductReport(
        seller_account_id=seller_account_id, 
        spreadsheet_name=spreadsheet_name, 
        worksheet_name=worksheet_name)
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity.id

def get_all_product_reports(db: Session) -> list[ProductReport]:
    return db.query(ProductReport).all()

def get_product_report_by_seller_account_id(db: Session, seller_account_id: int) -> ProductReport:
    return db.query(ProductReport).filter(ProductReport.seller_account_id == seller_account_id).all()

def get_product_report_by_id(db: Session, id: int) -> ProductReport:
    return db.query(ProductReport).filter(ProductReport.id == id).first()

def get_product_report_by_name(db: Session, name: str) -> ProductReport:
    return db.query(ProductReport).filter(ProductReport.name == name).first()

def update_product_report(db: Session, id: int, seller_account_id: int, spreadsheet_name: str, worksheet_name: str) -> ProductReport:
    entity = get_product_report_by_id(db, id)
    if entity:
        entity.seller_account_id = seller_account_id
        entity.spreadsheet_name = spreadsheet_name
        entity.worksheet_name = worksheet_name
        db.commit()
        db.refresh(entity)
    return entity

def delete_product_report(db: Session, id: int) -> bool:
    entity = get_product_report_by_id(db, id)
    if entity:
        db.delete(entity)
        db.commit()
        return True
    return False
