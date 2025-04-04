from datetime import datetime
from app.data_filler import fill_sheet_column
from app.date_formatter import DateFormatter

from_date = datetime(2025, 3, 24)
to_date = datetime(2025, 3, 26)
SPREADSHEET_NAME = "rnp-experiment"
WORKSHEET_NAME = "task"

report_dates = DateFormatter.generate_date_range(from_date, to_date)
report_dates
for report_date in report_dates:
    fill_sheet_column(SPREADSHEET_NAME, WORKSHEET_NAME, report_date)

