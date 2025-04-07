import logging
from app.table_filler import TableFiller
from app.date_formatter import DateFormatter
from app.infrastructure.logger import setup_logger
from app.infrastructure.config import get_config

setup_logger()
config = get_config()

SPREADSHEET_NAME = "rnp-experiment"
WORKSHEET_NAMES = [
    "Табурет стремянка деревянный подставка", 
    "Сумка A4 хобо через плечо",
    "Сумка маленькая дизайнерская"
]

if __name__ == "__main__":
    dates = DateFormatter.generate_date_range('01.03.2025', '31.03.2025')

    table_filler = TableFiller(config['api_token'], config['auth_cookies'])

    tables = table_filler.get_tables(SPREADSHEET_NAME, WORKSHEET_NAMES)
    all_nm_ids = table_filler.get_all_nm_ids()
    all_adv_ids = table_filler.get_all_adv_ids()

    for date in dates:
        table_filler.fill_tables_column(tables, all_nm_ids, all_adv_ids, date)
        logging.info(f'выгружены данные за {date.strftime("%d.%m.%Y")}')

