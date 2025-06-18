from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: str

    # читаем по отдельности из .env
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # pydantic v2: подключаем .env
    model_config = SettingsConfigDict(
        env_file             = ".env",
        env_file_encoding    = "utf-8",
        extra                = "ignore",  # игнорировать другие переменные
    )

    @property
    def DB_DSN(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

settings = Settings()