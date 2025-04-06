from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    API_ID: int
    API_HASH: str
    TOKEN_BOT: str
    WEBHOOK_TUNNEL_URL: str
    
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_PORT: int

    SECRET_KEY : str
    ALGORITHM : str

    MODEL : str
    HUGGING_ACCSES_TOKEN : str 

    @property
    def AsyncDataBaseUrl(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

