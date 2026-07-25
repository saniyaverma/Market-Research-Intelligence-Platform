from pydantic import BaseModel, Field

class Report(BaseModel):
    title: str
    executive_summary: str
    sections: list[str] = Field(default_factory=list)
    conclusion: str