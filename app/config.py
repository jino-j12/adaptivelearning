from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    MONGODB_URI: str = "mongodb://localhost:27017"
    DB_NAME: str = "adaptive_engine"

    GEMINI_API_KEY: str = ""

    INITIAL_ABILITY: float = 0.5
    MIN_ABILITY: float = 0.1
    MAX_ABILITY: float = 1.0

    DIFFICULTY_WINDOW: float = 0.2
    MAX_QUESTIONS: int = 10

    class Config:
        env_file = ".env"

settings = Settings()