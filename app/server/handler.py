from app.constructors.rnp import RnpConstructor
from app.server.model import WBAuthCookies

class Handler:
    def fill_range(self, date_from: str, date_to: str, api_token: str, auth_cookies: WBAuthCookies, google_sheets_creds, spreadsheet_name: str, worksheet_names: list[str]):
        rnp_constructor = RnpConstructor(auth_cookies, api_token, google_sheets_creds)
        
        rnp_constructor.fill_range(
            date_from, 
            date_to, 
            spreadsheet_name, 
            worksheet_names)     
