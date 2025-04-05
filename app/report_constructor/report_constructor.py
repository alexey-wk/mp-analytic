import pandas as pd
import numpy as np
from app.report_constructor.report_fields import REPORT_FIELDS, REPORT_FIELDS_ITEMS

pd.set_option('display.float_format', '{:.2f}'.format)

TAG_COL_IDX = 0
DATE_ROW_IDX = 1
NM_ID_ROW_IDX = 0
NM_ID_COL_IDX = 2
DISPLAY_TEXT_MAPPING = {field: info['display_text'] for field, info in REPORT_FIELDS.items()}

class ReportConstructor:
    def generate_stats_source_report(self, stats):
        df = pd.DataFrame(stats)
        df = df.abs()
        df = df.rename(index=DISPLAY_TEXT_MAPPING)
        df = df.sort_index(axis=1).reset_index()  
        df = df.rename(columns={'index': 'Метрики'})

        return df

    def generate_rnp_source(self, stats):
        df = pd.DataFrame(stats)
        df = df.abs()

        return df
    
    def find_tags_row_idxs(self, worksheet_rows):
        tag_row_idxs = {}
        for i, row in enumerate(worksheet_rows):
            cell = row[TAG_COL_IDX].strip().lower()

            for _, field in REPORT_FIELDS_ITEMS:
                if cell == field['tag']:
                    tag_row_idxs[cell] = i

        return tag_row_idxs.items()
    
    def find_date_col_idx(self, worksheet_rows, report_dot_date: str):
        for i, cell in enumerate(worksheet_rows[DATE_ROW_IDX]):
            if cell == report_dot_date:
                return i
        
        raise ValueError(f"Report date {report_dot_date} not found")
    
    def get_cell_value(self, nm_report, field_name, tag):
        value = nm_report.loc[field_name]
        if tag.endswith('_percent'):
            value = round(value/100, 2)

        if isinstance(value, np.generic):
            value = value.item()
        
        return value

    def get_nm_id(self, worksheet_rows):
        return int(worksheet_rows[NM_ID_ROW_IDX][NM_ID_COL_IDX])       
