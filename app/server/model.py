from pydantic import BaseModel
from typing import Union, Dict, Any


class WBAuthCookies(BaseModel):
    wbxValidationKey: str
    xSupplierIdExternal: str
    wbTokenV3: str


class FillRangeRequest(BaseModel):
    dateFrom: str
    dateTo: str
    apiToken: str
    authCookies: WBAuthCookies
    googleSheetsCreds: dict
    spreadsheetName: str
    worksheetNames: list[str]
