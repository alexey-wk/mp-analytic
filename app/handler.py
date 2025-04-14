import logging
from app.column_filler import ColumnFiller
from app.utils.date_formatter import DateFormatter
from app.server.model import WBAuthCookies


class Handler:
    def fill_range(self, date_from: str, date_to: str, api_token: str, auth_cookies: WBAuthCookies, google_sheets_creds_path: str, spreadsheet_name: str, worksheet_names: list[str]):
        dates = DateFormatter.generate_date_range(date_from, date_to)

        col_filler = ColumnFiller(
            api_token, 
            auth_cookies, 
            google_sheets_creds_path)

        tables = col_filler.get_tables(spreadsheet_name, worksheet_names)
        all_nm_ids = col_filler.get_all_nm_ids()
        all_adv_ids = col_filler.get_all_adv_ids()

        for date in dates:
            col_filler.fill_tables_column(tables, all_nm_ids, all_adv_ids, date)
            logging.info(f'выгружены данные за {date.strftime("%d.%m.%Y")}')

        logging.info('выгрузка завершена')

    def fill_range(self, date_from: str, date_to: str, api_token: str, auth_cookies: WBAuthCookies, google_sheets_creds, spreadsheet_name: str, worksheet_names: list[str]):
        dates = DateFormatter.generate_date_range(date_from, date_to)

        col_filler = ColumnFiller(
            api_token, 
            auth_cookies, 
            google_sheets_creds)

        tables = col_filler.get_tables(spreadsheet_name, worksheet_names)
        all_nm_ids = col_filler.get_all_nm_ids()
        all_adv_ids = col_filler.get_all_adv_ids()

        for date in dates:
            col_filler.fill_tables_column(tables, all_nm_ids, all_adv_ids, date)
            logging.info(f'выгружены данные за {date.strftime("%d.%m.%Y")}')

        logging.info('выгрузка завершена')
