from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.repository.db import Base

class ProductReport(Base):
    __tablename__ = "product_report"

    id = Column(Integer, primary_key=True, index=True)
    seller_account_id = Column(Integer, ForeignKey("seller_account.id"))
    spreadsheet_name = Column(String(128))
    worksheet_name = Column(String(128))
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"<ProductReport(id={self.id}, spreadsheet_name={self.spreadsheet_name}, worksheet_name={self.worksheet_name})>"
