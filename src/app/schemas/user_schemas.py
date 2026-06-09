from datetime import datetime

from pydantic import Field, SecretStr, field_validator

from .base import BaseSchema


class UserRegister(BaseSchema):
    username: str = Field(..., description="Username")
    password: SecretStr = Field(..., description="User password")

    @field_validator("password")
    @classmethod
    def not_empty(cls, v: SecretStr) -> SecretStr:
        if not v.get_secret_value().strip():
            raise ValueError("Password cannot be empty")
        return v

    @field_validator("username")
    @classmethod
    def no_spaces(cls, v: str) -> str:
        if " " in v:
            raise ValueError("Username must not have spaces")
        return v


class UserLogin(UserRegister):
    """The same that in register schema"""

    pass


class UserResponse(BaseSchema):
    id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    # There is no password hash
    is_active: bool = Field(..., description="User status")
    created_at: datetime = Field(..., description="User register time")
