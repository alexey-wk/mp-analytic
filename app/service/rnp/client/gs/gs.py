import gspread
import json
import base64
from oauth2client.service_account import ServiceAccountCredentials
from app.service.rnp.client.gs.contant import scope

class GoogleSheetsClient:
    def __init__(self, google_sa_creds: str):
        raw_creds = self.parse_creds(google_sa_creds)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(raw_creds, scope)    
        self.client = gspread.authorize(creds)
        
    def get_all_worksheets(self, spreadsheet_name: str):
        spreadsheet = self.client.open(spreadsheet_name)
        return spreadsheet.worksheets()

    def parse_creds(self, google_sa_creds: str):
        decoded_creds = base64.b64decode(google_sa_creds).decode('utf-8')
        creds_fixed = decoded_creds.replace('\n', '\\n')
        raw_creds = json.loads(creds_fixed)
        return raw_creds