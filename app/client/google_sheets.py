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

    def update_cell(self, spreadsheet_name, worksheet_name, row, col, value):
        client = gspread.authorize(self.creds)
        
        spreadsheet = client.open(spreadsheet_name)
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except:
            worksheet = spreadsheet.add_worksheet(
                title=worksheet_name, rows=max(row, 10), cols=max(col, 10))
                
        worksheet.update_cell(row, col, value)

    def update_cell_in_target_row(self, spreadsheet_name, worksheet_name, target_text, col_to_update, value):
        client = gspread.authorize(self.creds)
        
        spreadsheet = client.open(spreadsheet_name)
        worksheet = spreadsheet.worksheet(worksheet_name)        
        all_values = worksheet.get_all_values()
        
        target_row_index = None
        for i, row in enumerate(all_values):
            if len(row) >= 2 and row[1] == target_text:  # Check second column (index 1)
                target_row_index = i + 1  # Add 1 because gspread uses 1-based indexing
                break
        
        if target_row_index is None:
            raise ValueError(f"Could not find row with '{target_text}' in second column")
        
        # Update the specified cell in the target row
        worksheet.update_cell(target_row_index, col_to_update, value)
