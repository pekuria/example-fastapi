
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_PORT: str
    DATABASE_HOSTNAME: str
    DATABASE_NAME: str
    DATABASE_PASSWORD: str = "localhost"
    DATABASE_USERNAME: str = "petermutisya"
    SECRET_KEY: str = "CVXJNVLKXNVIXCIN39UQ9UE9UEQ9UQW90EUQWUEQ9W0UE9QWUE9Q0"
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = '.env'

settings = Settings()