from fastapi import APIRouter
from app.service.product_report.product_report import product_report_service
from app.controller.request.product_report import CreateProductReportRequest, UpdateProductReportRequest

product_report_router = APIRouter()

@product_report_router.post("/product-report/create")
async def create_product_report(req: CreateProductReportRequest):
    product_report_id = product_report_service.create_product_report(req)
    return {"product_report_id": product_report_id}

@product_report_router.post("/product-report/update")
async def update_product_report(req: UpdateProductReportRequest):
    updated_product_report = product_report_service.update_product_report(req)
    return updated_product_report
