from pydantic_settings import BaseSettings
from pydantic import BaseModel


class DBSettings(BaseModel):
    user: str
    password: str
    name: str
    host: str = "localhost"
    port: int = 5432

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
    
class JWTSetings(BaseModel):
    secret_key: str
    algorithm: str = 'HS256'


class Settings(BaseSettings):
    db: DBSettings
    jwt: JWTSetings

    model_config = {"env_file": ".env", "env_nested_delimiter": "__"}


settings = Settings()  # type: ignore
