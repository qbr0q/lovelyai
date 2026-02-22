from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict
from pydantic_settings_yaml import YamlBaseSettings


class AIConfig(BaseModel):
    base_url: str
    default_model: str


class Settings(YamlBaseSettings):
    ai: AIConfig

    model_config = SettingsConfigDict(
        yaml_file="settings.yml"
    )


settings = Settings()
