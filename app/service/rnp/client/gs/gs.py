import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from app.service.rnp.client.gs.contant import scope

class GoogleSheetsClient:
    def __init__(self, google_sa_creds: str):
        raw_creds = json.loads(google_sa_creds)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(raw_creds, scope)    
        self.client = gspread.authorize(creds)
        
    def get_all_worksheets(self, spreadsheet_name: str):
        spreadsheet = self.client.open(spreadsheet_name)
        return spreadsheet.worksheets()
