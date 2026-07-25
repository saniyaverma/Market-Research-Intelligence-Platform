from pydantic import BaseModel, Field
from uuid import uuid4


class ResearchTask(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    description: str
    status: str = "pending"