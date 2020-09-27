from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    test: bool = Field(False, env="CALORIE_TEST")
