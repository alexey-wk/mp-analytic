import datetime
import gspread
from gspread import Worksheet
from app.utils.date_formatter import DateFormatter
from app.client.wb.wb import WBClient
from app.client.gs.gs import GoogleSheetsClient
from app.extractors.advert import AdvertExtractor
from app.extractors.card import CardExtractor
from app.extractors.stock import StockExtractor
from app.extractors.finreport import FinReportExtractor
from app.aggregators.wb import WBAggregator
from app.report_constructor.report_fields import TAG_TO_FIELD_NAME
from app.report_constructor.report_constructor import ReportConstructor

class TableFiller:
    def __init__(self, api_token: str, auth_cookies: dict, google_sheets_creds_path: str):
        self.wb_client = WBClient(auth_cookies, api_token)
        self.gs_client = GoogleSheetsClient(google_sheets_creds_path)
        self.advFormatter = AdvertExtractor()
        self.cardFormatter = CardExtractor()
        self.stockFormatter = StockExtractor()
        self.finrepFormatter = FinReportExtractor()
        self.wbAggregator = WBAggregator()
        self.reportConstructor = ReportConstructor()
    
    def get_tables(self, spreadsheet_name: str, worksheet_names: list[str]):
        all_sheets = self.gs_client.get_all_worksheets(spreadsheet_name)
        return [
            sheet for sheet in all_sheets if sheet.title in worksheet_names
        ]
    
    def get_all_nm_ids(self):
        cards = self.wb_client.get_cards()
        return self.advFormatter.extract_nm_ids_from_cards_res(cards)
    
    def get_all_adv_ids(self):
        adv_auto, adv_auction = self.wb_client.get_adverts()
        adv_nms = self.advFormatter.group_nm_ids_by_adverts(adv_auto, adv_auction)
        return list(adv_nms.keys())

    def fill_tables_column(self, tables: list[Worksheet], all_nm_ids: list[int], all_adv_ids: list[int], report_date: datetime.datetime):
        # 1. Внутренний трафик по nm_id
        adv_stat = self.wb_client.get_adverts_stats(all_adv_ids, report_date)
        nm_adv_stats = self.advFormatter.extract_nm_stats_from_advs(adv_stat)
        
        # 2. Общий трафик (карточки) и выкупы по nm_id
        cards_stats = self.wb_client.get_cards_stats(all_nm_ids, report_date)
        nm_card_stats = self.cardFormatter.extract_nm_stats_from_cards_stats(cards_stats)

        # 3. Остатки по nm_id
        stocks = self.wb_client.get_stocks(all_nm_ids, report_date)
        nm_stock_stats = self.stockFormatter.extract_nm_stats_from_stocks(stocks)

        # 4. Расходы внутри маркетплейса по nm_id
        finreps = self.wb_client.get_finreports(report_date)
        finrep_ids = self.finrepFormatter.extract_finreport_ids(finreps)

        finrep_records = []
        for id in finrep_ids:
            finrep_stat = self.wb_client.get_finreport_stat_records(id)
            finrep_records.extend(finrep_stat)

        nm_finrep_stats = self.finrepFormatter.extract_nm_stats_from_finrep_records(finrep_records)

        # 5. Объединение всех данных по nm_id в финальный отчет
        combined_stats = self.wbAggregator.combine_stats(all_nm_ids, nm_adv_stats, nm_card_stats, nm_stock_stats, nm_finrep_stats)
        reports = self.reportConstructor.generate_rnp_source(combined_stats)

        report_dot_date = DateFormatter.get_dot_report_date(report_date)
        
        for table in tables:
            table_rows = table.get_all_values()
            tag_row_idxs = self.reportConstructor.find_tags_row_idxs(table_rows)
            date_col_idx = self.reportConstructor.find_date_col_idx(table_rows, report_dot_date)
            nm_id = self.reportConstructor.get_nm_id(table_rows)

            cell_updates = self._get_cell_updates(reports[nm_id], tag_row_idxs, date_col_idx)
            table.update_cells(cell_updates)

    def _get_cell_updates(self, nm_report, tag_row_idxs, col_idx):
        return [
            self._get_cell_update(nm_report, TAG_TO_FIELD_NAME[tag], tag, tag_idx, col_idx)
            for tag, tag_idx in tag_row_idxs 
            if self._is_to_update(tag, nm_report)
        ]
    
    def _is_to_update(self, tag, nm_report):
        return tag in TAG_TO_FIELD_NAME and TAG_TO_FIELD_NAME[tag] in nm_report.index

    def _get_cell_update(self, nm_report, field_name, tag, row_idx, col_idx):
        cell_value = self.reportConstructor.get_cell_value(nm_report, field_name, tag)
        return gspread.Cell(row_idx+1, col_idx+1, cell_value)
