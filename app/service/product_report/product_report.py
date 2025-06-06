from datetime import datetime
from app.controller.request.product_report import CreateProductReportRequest, UpdateProductReportRequest
from app.repository.product_report import create_product_report, update_product_report, get_all_product_reports
from app.repository.db import get_db

class ProductReportService:
    def create_product_report(self, req: CreateProductReportRequest):
        db = next(get_db())
        return create_product_report(
            db,
            req.sellerAccountId,
            req.spreadsheetName,
            req.worksheetName
        )

    def update_product_report(self, req: UpdateProductReportRequest):
        db = next(get_db())
        return update_product_report(
            db,
            req.id,
            req.sellerAccountId,
            req.spreadsheetName,
            req.worksheetName,
            datetime.now()
        )
    
    def get_all_product_reports(self):
        db = next(get_db())
        return get_all_product_reports(db)
    
product_report_service = ProductReportService()