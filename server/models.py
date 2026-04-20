from sqlalchemy import Column, Integer, String, DateTime, Text, func

from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(64), unique=True, nullable=False, comment="商品唯一编码")
    name = Column(String(100), nullable=False, comment="商品名称")
    image = Column(String(255), nullable=False, comment="商品图片文件名")
    description = Column(Text, nullable=True, comment="商品描述")
    sort_order = Column(Integer, nullable=False, default=0, comment="排序（升序）")
    created_at = Column(DateTime, server_default=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    openid = Column(String(64), unique=True, nullable=False, index=True, comment="微信用户openid")
    nickname = Column(String(100), nullable=False, comment="微信昵称")
    phone = Column(String(20), nullable=False, comment="手机号")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class UserSelection(Base):
    __tablename__ = "user_selections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    openid = Column(String(64), unique=True, nullable=False, index=True, comment="微信用户openid")
    product_code = Column(String(64), nullable=False, index=True, comment="商品唯一编码")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
