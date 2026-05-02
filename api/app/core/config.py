from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Pydantic BaseSettings automatski čita env varijable.
    """

    ENV: str = "dev"

    # Connection string za bazu.
    DATABASE_URL: str = "postgresql+asyncpg://pl_user:pl_pass@localhost:5432/pl_reg"

    # JWT Config
    JWT_SECRET: str = "change-me-in-production"
    JWT_ISSUER: str = "sit-unizd"

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173"

    # model_config govori Pydanticu ODAKLE čitati env varijable.
    # env_file=".env" znači: traži .env datoteku u working directoriju.
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

# Singleton instanca configa
settings = Settings()
