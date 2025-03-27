import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name(
    'sheet_creds.json', scope)


class GoogleSheetsClient:
    def __init__(self):
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            'sheet_creds.json', scope)

    def update_sheet(self, df, spreadsheet_name, worksheet_name):
        client = gspread.authorize(self.creds)

        spreadsheet = client.open(spreadsheet_name)
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except:
            worksheet = spreadsheet.add_worksheet(
                title=worksheet_name, rows=df.shape[0]+1, cols=df.shape[1]+2)

        worksheet.clear()

        data = [df.columns.tolist()] + df.values.tolist()
        worksheet.update(data)
