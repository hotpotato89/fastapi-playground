from pydantic_settings import BaseSettings
from pydantic import BaseModel


class DBConfig(BaseModel):
    user: str
    password: str
    name: str
    host: str = "localhost"
    port: int = 5432

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Config(BaseSettings):
    db: DBConfig

    model_config = {"env_file": ".env", "env_nested_delimiter": "__"}


settings = Config()  # type: ignore
