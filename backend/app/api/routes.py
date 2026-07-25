from fastapi import APIRouter
from pydantic import BaseModel

from app.services.adk_runner import run_root_agent

router = APIRouter()


class AnalyzeRequest(BaseModel):
    query: str


@router.post("/analyze")
async def analyze(request: AnalyzeRequest):
    answer = await run_root_agent(request.query)

    return {
        "response": answer
    }