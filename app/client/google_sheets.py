import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

class GoogleSheetsClient:
    def __init__(self, creds_path: str):
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        self.client = gspread.authorize(creds)
        
    def get_all_worksheets(self, spreadsheet_name: str):
        spreadsheet = self.client.open(spreadsheet_name)
        return spreadsheet.worksheets()
