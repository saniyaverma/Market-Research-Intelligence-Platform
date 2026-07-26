from pydantic import BaseModel, Field
from .evidence import Evidence

class Finding(BaseModel):
    title: str
    insight: str
    confidence: float = Field(ge=0.0, le=1.0)
    supporting_evidence: list[Evidence] = Field(default_factory=list)

class Findings(BaseModel):
    findings: list[Finding] = Field(default_factory=list)