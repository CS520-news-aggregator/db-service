import re
import uuid
from pydantic import BaseModel, EmailStr, Field, field_validator


class Token(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    user_id: str
    token: str

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": "sample",
                "token": "sample",
            }
        }


class RegisterUser(BaseModel):
    email_address: EmailStr
    password: str
    # first_name: str
    # last_name: str

    @field_validator("password")
    @classmethod
    def regex_match(cls, pwd: str) -> str:
        re_for_pwd: re.Pattern[str] = re.compile(
            r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        )
        if not re_for_pwd.match(pwd):
            raise ValueError(
                "Invalid password - must contain at least 1 letter and 1 number and"
                "be at least 8 characters long"
            )
        return pwd

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "email_address": "john_doe@gmail.com",
                "password": "password",
                # "first_name": "John",
                # "last_name": "Doe",
            }
        }


class LoginUser(BaseModel):
    email_address: EmailStr
    password: str

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "email_address": "john_doe@gmail.com",
                "password": "password",
            }
        }


class Preferences(BaseModel):
    preferences: list[str]

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "preferences": ["sports", "food", "mastering the art of getting bored"]
            }
        }

