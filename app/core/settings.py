from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict
from pydantic_settings_yaml import YamlBaseSettings


class AISettings(BaseModel):
    base_url: str
    default_model: str
    embedder_model: str
    daily_limit: int


class GARSettings(BaseModel):
    base_url: str
    user_agent: str


class ChannelSettings(BaseModel):
    id: int
    url: str


class Settings(YamlBaseSettings):
    ai: AISettings
    gar: GARSettings
    channel: ChannelSettings
    use_proxy: bool = Field(validation_alias="use_proxy")

    model_config = SettingsConfigDict(
        yaml_file="settings.yml"
    )


settings = Settings()
