from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class PostgresConfig(BaseModel):
    name: str
    user: str
    password: str
    host: str
    port: int

    @property
    def url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name
        )


class TokenConfig(BaseModel):
    expire_hours: int


class RedisConfig(BaseModel):
    password: str
    host: str
    port: int
    db:int

    @property
    def url(self) -> str:
        return  f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_nested_delimiter="__",
        extra="ignore",
    )

    db: PostgresConfig = Field(default_factory=PostgresConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    token: TokenConfig = Field(default_factory=TokenConfig)


settings = Settings()
