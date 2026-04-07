import httpx
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from config import API_PREFIX, STATIC_PREFIX, WX_APPID, WX_SECRET
from database import engine, get_db, Base
from models import Product, User, UserSelection
from schemas import (
    ProductOut,
    UserSelectionIn,
    UserSelectionOut,
    WxLoginRequest,
    WxPhoneRequest,
    MessageResponse,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MetLife API", docs_url=f"{API_PREFIX}/docs", openapi_url=f"{API_PREFIX}/openapi.json")

app.mount(STATIC_PREFIX, StaticFiles(directory="static"), name="static")


# ==================== 微信相关接口 ====================

@app.post(f"{API_PREFIX}/wx/login")
async def wx_login(req: WxLoginRequest):
    """用 wx.login 的 code 换取 openid"""
    url = "https://api.weixin.qq.com/sns/jscode2session"
    params = {
        "appid": WX_APPID,
        "secret": WX_SECRET,
        "js_code": req.code,
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        data = resp.json()
    if "openid" not in data:
        raise HTTPException(status_code=400, detail=data.get("errmsg", "微信登录失败"))
    return {"openid": data["openid"], "session_key": data["session_key"]}


@app.post(f"{API_PREFIX}/wx/phone")
async def wx_get_phone(req: WxPhoneRequest):
    """用 getPhoneNumber 的 code 换取手机号"""
    token_url = "https://api.weixin.qq.com/cgi-bin/token"
    token_params = {
        "grant_type": "client_credential",
        "appid": WX_APPID,
        "secret": WX_SECRET,
    }
    async with httpx.AsyncClient() as client:
        token_resp = await client.get(token_url, params=token_params)
        token_data = token_resp.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="获取access_token失败")

        phone_url = f"https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token={access_token}"
        phone_resp = await client.post(phone_url, json={"code": req.code})
        phone_data = phone_resp.json()

    if phone_data.get("errcode") != 0:
        raise HTTPException(status_code=400, detail=phone_data.get("errmsg", "获取手机号失败"))
    return {"phone": phone_data["phone_info"]["phoneNumber"]}


# ==================== 商品接口 ====================

@app.get(f"{API_PREFIX}/products", response_model=list[ProductOut])
def get_products(db: Session = Depends(get_db)):
    """获取所有商品列表"""
    products = db.query(Product).all()
    result = []
    for p in products:
        out = ProductOut.model_validate(p)
        out.image_url = f"{STATIC_PREFIX}/{p.image}"
        result.append(out)
    return result


# ==================== 用户选择接口 ====================

@app.get(f"{API_PREFIX}/selection/{{openid}}", response_model=UserSelectionOut | None)
def get_selection(openid: str, db: Session = Depends(get_db)):
    """查询用户是否已选择过商品"""
    user = db.query(User).filter(User.openid == openid).first()
    if not user:
        return None
    selection = db.query(UserSelection).filter(UserSelection.user_id == user.id).first()
    if not selection:
        return None
    return UserSelectionOut(
        openid=user.openid,
        nickname=user.nickname,
        phone=user.phone,
        product_id=selection.product_id,
    )


@app.post(f"{API_PREFIX}/selection", response_model=MessageResponse)
def submit_selection(data: UserSelectionIn, db: Session = Depends(get_db)):
    """提交或更新用户商品选择"""
    # 检查商品是否存在
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")

    # 查找或创建用户
    user = db.query(User).filter(User.openid == data.openid).first()
    if user:
        user.nickname = data.nickname
        user.phone = data.phone
    else:
        user = User(openid=data.openid, nickname=data.nickname, phone=data.phone)
        db.add(user)
        db.flush()

    # 查找或创建选择记录
    selection = db.query(UserSelection).filter(UserSelection.user_id == user.id).first()
    if selection:
        selection.product_id = data.product_id
        db.commit()
        return MessageResponse(message="已更新您的商品选择")

    selection = UserSelection(user_id=user.id, product_id=data.product_id)
    db.add(selection)
    db.commit()
    return MessageResponse(message="提交成功，感谢您的参与！")
