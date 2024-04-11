import uuid
from pydantic import BaseModel, Field
from typing import List


class Annotation(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    post_id: str
    list_topics: List[str]

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {"post_id": "sample", "list_topics": ["sample"]}
        }
