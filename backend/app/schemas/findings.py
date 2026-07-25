from pydantic import BaseModel, Field
from .evidence import Evidence

class Finding(BaseModel):
    statement: str
    supporting_evidence: list[Evidence] = Field(default_factory=list)
    confidence: float