from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "development"
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/civicpulse"
    REDIS_URL: str = "redis://localhost:6379/0"
    TRIAGE_PROVIDER: str = "rules"
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    RATE_LIMIT_PER_MINUTE: int = 200
    
    class Config:
        env_file = ".env"

settings = Settings()
