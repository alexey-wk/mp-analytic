from pydantic import BaseModel
from app.controller.request.request import WBAuthCookies

class FillRangeRequest(BaseModel):
    dateFrom: str
    dateTo: str
    apiToken: str
    authCookies: WBAuthCookies
    spreadsheetName: str
    worksheetNames: list[str]
