import uuid
from pydantic import BaseModel, Field
from typing import List


class Annotation(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    post_ids: List[str]
    topics: List[str]

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {"post_ids": ["sample"], "topics": ["sample"]}
        }
