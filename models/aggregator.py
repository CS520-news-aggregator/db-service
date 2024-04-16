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


class Comment(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    content: str
    post_id: str

    upvotes: int = 0
    downvotes: int = 0

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "content": "sample",
                "post_id": "sample",
            }
        }
