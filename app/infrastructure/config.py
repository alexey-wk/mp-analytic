import os
from dotenv import load_dotenv

load_dotenv()

def get_config():
    return {
        'api_token': os.getenv("API_TOKEN"),
        'auth_cookies': {
            'wbx-validation-key': os.getenv('WBX_VALIDATION_KEY'),
            'x-supplier-id-external': os.getenv('X_SUPPLIER_ID_EXTERNAL'),
            'WBTokenV3': os.getenv('WB_TOKEN_V3'),
        },
        'google_sheets_creds_path': 'sheet_creds.json',
    }
