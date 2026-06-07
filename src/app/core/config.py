from pydantic_settings import BaseSettings
from pydantic import BaseModel


class DBConfig(BaseModel):
    user: str
    password: str
    name: str


class Config(BaseSettings):
    db: DBConfig

    model_config = {"env_file": ".env", "env_nested_delimiter": "__"}


config = Config()  # type: ignore
