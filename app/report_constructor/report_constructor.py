import pandas as pd
from app.report_constructor.report_fields import REPORT_FIELDS

pd.set_option('display.float_format', '{:.2f}'.format)

display_text_mapping = {field: info['display_text'] for field, info in REPORT_FIELDS.items()}

class ReportConstructor:
    def generate_stats_source_report(self, stats):
        df = pd.DataFrame(stats)
        df = df.abs()
        df = df.rename(index=display_text_mapping)
        df = df.sort_index(axis=1).reset_index()  
        df = df.rename(columns={'index': 'Метрики'})

        return df

    def generate_rnp_source(self, stats):
        df = pd.DataFrame(stats)
        df = df.abs()

        return df
