from pydantic import BaseModel, Field

class ReportSection(BaseModel):
    heading: str
    content: str

class Report(BaseModel):
    title: str
    executive_summary: str
    sections: list[ReportSection] = Field(default_factory=list)
    conclusion: str