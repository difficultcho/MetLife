from pydantic import BaseModel
from typing import Optional


class ProductOut(BaseModel):
    id: int
    code: str
    name: str
    image: str
    image_url: str = ""
    description: Optional[str] = None
    sort_order: int

    model_config = {"from_attributes": True}


class UserSelectionIn(BaseModel):
    openid: str
    nickname: str
    phone: str
    product_code: str


class UserSelectionOut(BaseModel):
    openid: str
    nickname: str
    phone: str
    product_code: str

    model_config = {"from_attributes": True}


class WxLoginRequest(BaseModel):
    code: str


class WxPhoneRequest(BaseModel):
    code: str


class MessageResponse(BaseModel):
    message: str


class PageConfigOut(BaseModel):
    bg_image: str
    banner_text: str
