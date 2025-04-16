import datetime
import gspread
import logging
import numpy as np
from gspread import Worksheet
from app.utils.date_formatter import DateFormatter
from app.client.wb.wb import WBClient
from app.client.gs.gs import GoogleSheetsClient
from app.extractors.advert import AdvertExtractor
from app.extractors.card import CardExtractor
from app.extractors.stock import StockExtractor
from app.extractors.finreport import FinReportExtractor
from app.aggregators.wb import WBAggregator
from app.server.model import WBAuthCookies
from .constant import TAG_TO_FIELD_NAME
from .constant import REPORT_FIELDS_ITEMS, TAG_COL_IDX, DATE_ROW_IDX, NM_ID_ROW_IDX, NM_ID_COL_IDX


class RnpConstructor:
    def __init__(self, auth_cookies: WBAuthCookies, api_token: str, google_sheets_creds: dict):
        self.wb_client = WBClient(auth_cookies, api_token)
        self.gs_client = GoogleSheetsClient(google_sheets_creds)
        self.adv_extractor = AdvertExtractor()
        self.card_extractor = CardExtractor()
        self.stock_extractor = StockExtractor()
        self.finrep_extractor = FinReportExtractor()
        self.wb_aggregator = WBAggregator()
    

    def fill_range(self, date_from: str, date_to: str, spreadsheet_name: str, worksheet_names: list[str]):
        logging.info('начало извлечения данных')

        sheets = self.get_sheets(spreadsheet_name, worksheet_names)
        nm_ids = self.get_all_nm_ids()
        adv_ids = self.get_all_adv_ids()

        dates = DateFormatter.generate_date_range(date_from, date_to)
        for date in dates:
            self.fill_sheets_column(sheets, nm_ids, adv_ids, date)
            logging.info(f'внесены в таблицу данные за {date.strftime("%d.%m.%Y")}')

        logging.info('извлечение данных завершено')


    def get_sheets(self, filename: str, sheet_names: list[str]):
        all_sheets = self.gs_client.get_all_worksheets(filename)
        return [
            sheet for sheet in all_sheets if sheet.title in sheet_names
        ]
    

    def get_all_nm_ids(self):
        cards = self.wb_client.get_cards()
        return self.adv_extractor.extract_nm_ids_from_cards_res(cards)
    

    def get_all_adv_ids(self):
        advs = self.wb_client.get_adverts()
        return self.adv_extractor.get_all_adv_ids(advs)


    def fill_sheets_column(self, sheets: list[Worksheet], all_nm_ids: list[int], all_adv_ids: list[int], report_date: datetime.datetime):
        # 1. Внутренний трафик по nm_id
        adv_stat = self.wb_client.get_adverts_stats(all_adv_ids, report_date)
        nm_adv_stats = self.adv_extractor.extract_nm_stats_from_advs(adv_stat)
        
        # 2. Общий трафик карточки и выкупы по nm_id
        cards_stats = self.wb_client.get_cards_stats(all_nm_ids, report_date)
        nm_card_stats = self.card_extractor.extract_nm_stats_from_cards_stats(cards_stats)

        # 3. Остатки по nm_id
        stocks = self.wb_client.get_stocks(all_nm_ids, report_date)
        nm_stock_stats = self.stock_extractor.extract_nm_stats_from_stocks(stocks)

        # 4. Расходы внутри маркетплейса по nm_id
        finreps = self.wb_client.get_finreports(report_date)
        nm_finrep_stats = self.get_finrep_stats(finreps)

        # 5. Объединение всех данных по nm_id в финальный отчет
        aggregated_stats = self.wb_aggregator.aggregate_stats(all_nm_ids, nm_adv_stats, nm_card_stats, nm_stock_stats, nm_finrep_stats)

        report_dot_date = DateFormatter.get_dot_report_date(report_date)
        for sheet in sheets:
            self.fill_sheet_column(sheet, aggregated_stats, report_dot_date)


    def get_finrep_stats(self, finreps: list[dict]):
        finrep_ids = self.finrep_extractor.extract_finrep_ids(finreps)

        finrep_records = []
        for id in finrep_ids:
            finrep_stat = self.wb_client.get_finreport_stat_records(id)
            finrep_records.extend(finrep_stat)

        return self.finrep_extractor.extract_nm_stats_from_finrep_records(finrep_records)


    def fill_sheet_column(self, sheet: Worksheet, aggregated_stats: dict, dot_date: str):
        rows = sheet.get_all_values()
        tag_row_idxs = self._find_tags_row_idxs(rows)
        date_col_idx = self._find_date_col_idx(rows, dot_date)
        nm_id = self._get_nm_id(rows)

        cell_updates = self._get_cell_updates(aggregated_stats[nm_id], tag_row_idxs, date_col_idx)
        sheet.update_cells(cell_updates)


    def _find_tags_row_idxs(self, worksheet_rows):
        tag_row_idxs = {}
        for i, row in enumerate(worksheet_rows):
            cell = row[TAG_COL_IDX].strip().lower()

            for _, field in REPORT_FIELDS_ITEMS:
                if cell == field['tag']:
                    tag_row_idxs[cell] = i

        return tag_row_idxs.items()


    def _find_date_col_idx(self, worksheet_rows, report_dot_date: str):
        for i, cell in enumerate(worksheet_rows[DATE_ROW_IDX]):
            if cell == report_dot_date:
                return i
        
        raise ValueError(f"Report date {report_dot_date} not found")
    

    def _get_nm_id(self, worksheet_rows):
        return int(worksheet_rows[NM_ID_ROW_IDX][NM_ID_COL_IDX])       


    def _get_cell_updates(self, nm_report, tag_row_idxs, col_idx):
        return [
            self._get_cell_updated_val(nm_report, TAG_TO_FIELD_NAME[tag], tag, tag_idx, col_idx)
            for tag, tag_idx in tag_row_idxs 
            if self._is_to_update(tag, nm_report)
        ]


    def _is_to_update(self, tag, nm_report):
        return tag in TAG_TO_FIELD_NAME and TAG_TO_FIELD_NAME[tag] in nm_report.index


    def _get_cell_updated_val(self, nm_report, field_name, tag, row_idx, col_idx):
        cell_value = self._standardize_val(nm_report, field_name, tag)
        return gspread.Cell(row_idx+1, col_idx+1, cell_value)


    def _standardize_val(self, nm_report, field_name, tag):
        value = nm_report.loc[field_name]
        if tag.endswith('_percent'):
            value = round(value/100, 2)

        if isinstance(value, np.generic):
            value = value.item()
        
        return value
