from pydantic import BaseModel
from typing import Optional


class ProductOut(BaseModel):
    id: int
    name: str
    image: str
    image_url: str = ""
    description: Optional[str] = None

    model_config = {"from_attributes": True}


class UserSelectionIn(BaseModel):
    openid: str
    nickname: str
    phone: str
    product_id: int


class UserSelectionOut(BaseModel):
    openid: str
    nickname: str
    phone: str
    product_id: int

    model_config = {"from_attributes": True}


class WxLoginRequest(BaseModel):
    code: str


class WxPhoneRequest(BaseModel):
    code: str


class MessageResponse(BaseModel):
    message: str
