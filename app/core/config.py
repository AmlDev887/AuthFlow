from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr

class Settings():
    
    SECRET_KEY:str
    SENDER:EmailStr
    SMTP_URL:str

    EMAIL:EmailStr
    PASSWORD:str

    DB_PASSWORD="amalbek2004"
    DB_HOST="localhost"
    DB_PORT=5432
    DB_NAME="train"
    DATABASE="postgres"

    REDIS_URL = str

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8"
        )
settings = Settings()
    