from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict
from pydantic_settings_yaml import YamlBaseSettings


class AISettings(BaseModel):
    base_url: str
    default_model: str


class GARSettings(BaseModel):
    base_url: str
    user_agent: str


class Settings(YamlBaseSettings):
    ai: AISettings
    gar: GARSettings
    use_proxy: bool = Field(validation_alias="use_proxy")

    model_config = SettingsConfigDict(
        yaml_file="settings.yml"
    )


settings = Settings()
