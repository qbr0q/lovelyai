from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PrivateConfig(BaseModel):
    bot_token: str
    support_bot_token: str
    openrouter_api_key: str


class DBConfig(BaseModel):
    user: str
    password: str
    host: str
    port: int
    db: str

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class ProxyConfig(BaseModel):
    login: str
    password: str
    ip: str
    port: int

    @property
    def url(self):
        return f"socks5://{self.login}:{self.password}@{self.ip}:{self.port}"


class RedisConfig(BaseModel):
    host: str
    port: str
    db: str

    @property
    def url(self):
        return f"redis://{self.host}:{self.port}/{self.db}"


class Config(BaseSettings):
    private: PrivateConfig
    db: DBConfig
    proxy: ProxyConfig
    redis: RedisConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__"
    )


config = Config()
