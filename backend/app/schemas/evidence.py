from pydantic import BaseModel

class Evidence(BaseModel):
    task_id: str
    claim: str
    summary: str
    source: str
    url: str