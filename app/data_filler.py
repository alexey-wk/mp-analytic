import os
import datetime
import logging
from app.date_formatter import DateFormatter
from app.client.wb import WBClient
from app.client.google_sheets import GoogleSheetsClient
from app.extractors.advert import AdvertFormatter
from app.extractors.card import CardFormatter
from app.extractors.finreport import FinReportFormatter
from app.stat_aggregator import StatAggregator
from app.report_constructor.report_fields import TAG_TO_FIELD_NAME
from app.report_constructor.report_constructor import ReportConstructor
from dotenv import load_dotenv
import gspread

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
AUTH_COOKIES = {
    'wbx-validation-key': os.getenv('WBX_VALIDATION_KEY'),
    'x-supplier-id-external': os.getenv('X_SUPPLIER_ID_EXTERNAL'),
    'WBTokenV3': os.getenv('WB_TOKEN_V3'),
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True 
)

class DataFiller:
    def __init__(self):
        self.wb_client = WBClient(AUTH_COOKIES, API_TOKEN)
        self.gs_client = GoogleSheetsClient()
        self.advFormatter = AdvertFormatter()
        self.cardFormatter = CardFormatter()
        self.finrepFormatter = FinReportFormatter()
        self.statAggregator = StatAggregator()
        self.reportConstructor = ReportConstructor()

    def fill_sheet_column(self, spreadsheet_name: str, worksheet_name: str, report_date: datetime.datetime):
        # Получение выбранного листа таблицы и nm_id
        worksheet = self.gs_client.get_worksheet(spreadsheet_name, worksheet_name)
        worksheet_rows = worksheet.get_all_values()
        nm_id = self.reportConstructor.get_nm_id(worksheet_rows)
        
        # 1. nm_id всех карточек продавца
        cards = self.wb_client.get_cards()
        nm_ids = self.advFormatter.extract_nm_ids_from_cards(cards)

        # 2. Внутренний трафик по nm_id
        adv_auto, adv_auction = self.wb_client.get_adverts()
        adv_nms = self.advFormatter.group_nm_ids_by_adverts(adv_auto, adv_auction)
        adv_ids = list(adv_nms.keys())
        adv_stat = self.wb_client.get_adverts_stats(adv_ids, report_date)
        nm_adv_stats = self.advFormatter.extract_nm_stats_from_advs(adv_stat)
        
        # 3. Общий трафик (карточки), остатки и выкупы по nm_id
        cards_stats = self.wb_client.get_cards_stats(nm_ids, report_date)
        nm_card_stats = self.cardFormatter.extract_nm_stats_from_cards(cards_stats)

        # 4. Расходы внутри маркетплейса по nm_id
        finreps = self.wb_client.get_finreports(report_date)
        finrep_ids = self.finrepFormatter.extract_finreport_ids(finreps)

        finrep_records = []
        for id in finrep_ids:
            finrep_stat = self.wb_client.get_finreport_stat_records(id)
            finrep_records.extend(finrep_stat)

        nm_finrep_stats = self.finrepFormatter.extract_nm_stats_from_finrep_records(finrep_records)

        # 5. Объединение всех данных по nm_id в финальный отчет
        combined_stats = self.statAggregator.combine_stats(nm_adv_stats, nm_card_stats, nm_finrep_stats)

        reports = self.reportConstructor.generate_rnp_source(combined_stats)

        report_dot_date = DateFormatter.get_dot_report_date(report_date)
        tag_row_idxs = self.reportConstructor.find_tags_row_idxs(worksheet_rows)
        date_col_idx = self.reportConstructor.find_date_col_idx(worksheet_rows, report_dot_date)
        nm_report = reports[nm_id]

        cell_updates = []

        for row_tag, row_idx in tag_row_idxs:
            if row_tag not in TAG_TO_FIELD_NAME:
                continue
            
            field_name = TAG_TO_FIELD_NAME[row_tag]
            if field_name in nm_report.index:
                cell_coords = self.reportConstructor.get_cell_coords(row_idx, date_col_idx)
                cell_value = self.reportConstructor.get_cell_value(nm_report, field_name, row_tag)

                cell_updates.append((cell_coords[0], cell_coords[1], cell_value))

        cells = [gspread.Cell(row, col, value) for row, col, value in cell_updates]
        worksheet.update_cells(cells)

