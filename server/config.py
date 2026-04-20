import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "metlife")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

WX_APPID = os.getenv("WX_APPID", "")
WX_SECRET = os.getenv("WX_SECRET", "")

API_PREFIX = os.getenv("API_PREFIX", "")
STATIC_PREFIX = os.getenv("STATIC_PREFIX", "/static")

# 页面配置（发版常量，变更需重启服务）
BG_IMAGE = "bg.png"
BANNER_TEXT = "世界杯精彩好礼等你拿"
