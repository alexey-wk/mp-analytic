from pydantic import BaseModel
from datetime import datetime

class CreateProductReportRequest(BaseModel):
    sellerAccountId: int
    spreadsheetName: str
    worksheetName: str


class UpdateProductReportRequest(BaseModel):
    id: int
    sellerAccountId: int
    spreadsheetName: str
    worksheetName: str

class DeleteProductReportRequest(BaseModel):
    id: int 

class GetProductReportRequest(BaseModel):
    id: int

