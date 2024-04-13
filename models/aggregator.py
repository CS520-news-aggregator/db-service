import uuid
from pydantic import BaseModel, Field


class Post(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str
    link: str
    media: str
    author: str
    date: str

    upvotes: int = 0
    downvotes: int = 0
    comments: list = []

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "title": "sample",
                "link": "sample",
                "media": "sample",
                "author": "sample",
                "date": "sample",
            }
        }
