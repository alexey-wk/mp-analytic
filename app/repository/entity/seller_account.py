from sqlalchemy import Column, Integer, String, JSON
from app.repository.db import Base

class SellerAccount(Base):
    __tablename__ = "seller_account"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128))
    api_token = Column(String(512), nullable=False)
    auth_cookies = Column(JSON, nullable=False)

    def __repr__(self):
        return f"<SellerAccount(id={self.id}, name={self.name})>"
