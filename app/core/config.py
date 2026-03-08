from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseModel):
    user: str
    password: str
    host: str
    port: int
    db: str


class Config(BaseSettings):
    bot_token: str = Field(validation_alias="BOT_TOKEN")
    openrouter_api_key: str = Field(validation_alias="OPENROUTER_API_KEY")
    db: DBSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="_"
    )


config = Config()
