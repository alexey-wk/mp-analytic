from pydantic import BaseModel

class CreateSellerAccountRequest(BaseModel):
    name: str
    apiToken: str
    authCookies: dict

class UpdateSellerAccountRequest(BaseModel):
    id: int
    name: str
    apiToken: str
    authCookies: dict

class DeleteSellerAccountRequest(BaseModel):
    id: int 

class GetSellerAccountRequest(BaseModel):
    id: int

