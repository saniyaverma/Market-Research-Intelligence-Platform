from pydantic import BaseModel, Field
from .research_task import ResearchTask

class ResearchPlan(BaseModel):
    objective: str
    information_needed: list[str] = Field(default_factory=list)
    tasks: list[ResearchTask] = Field(default_factory=list)
    deliverables: list[str] = Field(default_factory=list)