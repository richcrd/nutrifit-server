from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60 * 24
    jwt_refresh_expiration_days: int = 7
    cors_origin: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    def get_cors_list(self):
        if self.cors_origin == "":
            return []
        else:
            return self.cors_origin.split(",")

settings = Settings()