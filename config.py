from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

#  class TelegramConfig(BaseModel):


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", ".env.local"))

    tg_model_apikey: str = Field(alias='TG_BOT_APIKEY')
    #  tg_model: TelegramConfig = TelegramConfig()

settings = Settings()
