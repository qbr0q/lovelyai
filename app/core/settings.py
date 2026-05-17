from pydantic import BaseModel
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


class SocialSettings(BaseModel):
    public_channel_id: int
    public_channel_url: str
    staff_channel_id: int


class Settings(YamlBaseSettings):
    ai: AISettings
    gar: GARSettings
    social: SocialSettings
    use_proxy: bool

    model_config = SettingsConfigDict(
        yaml_file="settings.yml"
    )


settings = Settings()
