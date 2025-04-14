import os
from dotenv import load_dotenv
from app.server.model import WBAuthCookies

load_dotenv()

def get_config():
    return {
        'api_token': os.getenv('API_TOKEN'),
        'auth_cookies': WBAuthCookies(
            os.getenv('WBX_VALIDATION_KEY'),
            os.getenv('X_SUPPLIER_ID_EXTERNAL'),
            os.getenv('WB_TOKEN_V3'),
        ),
        'google_sheets_creds': os.getenv('GOOGLE_SHEETS_CREDS'),
    }
