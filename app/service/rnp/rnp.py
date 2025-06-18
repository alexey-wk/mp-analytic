import os
from datetime import date, datetime, timedelta
from app.service.rnp.constructors.rnp import RnpConstructor
from app.controller.request.request import WBAuthCookies
from app.utils.date_formatter import DateFormatter
from app.repository.db import get_db
from app.repository.seller_account import get_all_seller_accounts
from app.repository.product_report import get_product_report_by_seller_account_id
from app.repository.entity.seller_account import SellerAccount
from app.config import config
import asyncio

class RnpService:
    def fill_range_by_req(self, date_from_str: str, date_to_str: str, api_token: str, auth_cookies: WBAuthCookies, spreadsheet_name: str, worksheet_names: list[str]):
        rnp_constructor = RnpConstructor(auth_cookies, api_token, config.GOOGLE_SA_CREDS)
        
        range_start = DateFormatter.parse_dot_date(date_from_str)
        range_end = DateFormatter.parse_dot_date(date_to_str)

        rnp_constructor.fill_range(
            range_start, 
            range_end, 
            spreadsheet_name, 
            worksheet_names)    

    def fill_range_by_job(self, date_from: date, date_to: date, api_token: str, auth_cookies: WBAuthCookies, spreadsheet_name: str, worksheet_names: list[str]):
        rnp_constructor = RnpConstructor(auth_cookies, api_token, config.GOOGLE_SA_CREDS)
        
        rnp_constructor.fill_range(
            date_from, 
            date_to, 
            spreadsheet_name, 
            worksheet_names)
    
    async def update_all_reports(self):
        db = next(get_db())
        seller_accounts = get_all_seller_accounts(db) 

        tasks = [self.update_account_reports(account) for account in seller_accounts]
        await asyncio.gather(*tasks)

    def update_account_reports(self, account: SellerAccount):
        db = next(get_db())
        curr_date = datetime.now().date()
        seven_days_ago = curr_date - timedelta(days=7)
        product_reports = get_product_report_by_seller_account_id(db, account.id)

        for report in product_reports:
            self.fill_range_by_job(
                seven_days_ago, 
                curr_date,
                account.api_token, 
                account.auth_cookies, 
                report.spreadsheet_name, 
                report.worksheet_name
            )


rnp_service = RnpService()
