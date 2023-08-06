from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str
    DB_NAME: str = "test"
    # COLLECTION_NAME: str = "flashcards"

    class Config:
        env_file = '../.env'


settings = Settings()
