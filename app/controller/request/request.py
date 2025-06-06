from pydantic import BaseModel

class WBAuthCookies(BaseModel):
    authorizev3: str
    wbxValidationKey: str
    xSupplierIdExternal: str
    wbTokenV3: str
