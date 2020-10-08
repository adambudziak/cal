from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    test: bool = Field(False, env="CALORIE_TEST")
    debug: bool = Field(False, env="DEBUG")


app_settings = AppSettings()
