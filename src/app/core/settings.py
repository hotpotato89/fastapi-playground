from pathlib import Path

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


class JWTSettings(BaseModel):
    algorithm: str = 'RS256'
    private_key_path: Path
    public_key_path: Path


class DeploySettings(BaseModel):
    allow_origins: list[str] = ["*"]
    allow_credentials: bool = False
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["Content-Type", "Authorization"]


class Settings(BaseSettings):
    db: DBSettings
    jwt: JWTSettings
    deploy: DeploySettings

    model_config = {"env_file": ".env", "env_nested_delimiter": "__"}


settings = Settings()  # type: ignore
