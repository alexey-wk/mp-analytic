import os
from dotenv import load_dotenv
from app.server.model import WBAuthCookies

load_dotenv()

def get_config():
    cookies = WBAuthCookies(
        wbxValidationKey=os.getenv('WBX_VALIDATION_KEY'),
        xSupplierIdExternal=os.getenv('X_SUPPLIER_ID_EXTERNAL'),
        wbTokenV3=os.getenv('WB_TOKEN_V3'),
    )

    return {
        'api_token': os.getenv('API_TOKEN'),
        'auth_cookies': cookies,
        'google_sheets_creds_path': os.getenv('GOOGLE_SHEETS_CREDS_PATH'),
    }
