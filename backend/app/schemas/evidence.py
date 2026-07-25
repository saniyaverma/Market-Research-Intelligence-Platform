from pydantic import BaseModel

class Evidence(BaseModel):
    claim: str
    source: str
    url: str
    summary: str