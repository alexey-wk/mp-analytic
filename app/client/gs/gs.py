import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app.client.gs.contant import scope

class GoogleSheetsClient:
    def __init__(self, creds: dict):
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds, scope)    
        self.client = gspread.authorize(creds)
        
    def get_all_worksheets(self, spreadsheet_name: str):
        spreadsheet = self.client.open(spreadsheet_name)
        return spreadsheet.worksheets()
