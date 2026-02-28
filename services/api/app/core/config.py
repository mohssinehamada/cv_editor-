from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Resume-JD Matcher API"


settings = Settings()
