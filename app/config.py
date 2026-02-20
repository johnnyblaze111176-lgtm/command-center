from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    jwt_secret: str
    admin_email: str = "admin@example.com"
    admin_password: str = "ChangeMeNow123!"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    database_url: str = "sqlite:///./command_center.db"

settings = Settings()
