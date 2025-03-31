from zoneinfo import ZoneInfo
from environs import Env

env = Env()
env.read_env()


class Settings:
    TIMEZONE = ZoneInfo("Asia/Tashkent")
    JWT_SECRET_KEY = env.str("JWT_SECRET_KEY")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRY_MINUTES = 30


settings = Settings()
