from typing import List
from pydantic import BaseModel, Field
from .evidence import Evidence

class Finding(BaseModel):
    title: str
    insight: str
    confidence: float
    supporting_evidence: List[Evidence] = Field(default_factory=list)