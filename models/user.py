import uuid
from pydantic import BaseModel, EmailStr, Field


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
