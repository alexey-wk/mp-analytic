from app.constructors.rnp import RnpConstructor
from app.server.model import WBAuthCookies
from app.utils.date_formatter import DateFormatter


class Handler:
    def fill_range(self, date_from_str: str, date_to_str: str, api_token: str, auth_cookies: WBAuthCookies, google_sheets_creds, spreadsheet_name: str, worksheet_names: list[str]):
        rnp_constructor = RnpConstructor(auth_cookies, api_token, google_sheets_creds)
        
        range_start = DateFormatter.parse_dot_date(date_from_str)
        range_end = DateFormatter.parse_dot_date(date_to_str)

        rnp_constructor.fill_range(
            range_start, 
            range_end, 
            spreadsheet_name, 
            worksheet_names)     
