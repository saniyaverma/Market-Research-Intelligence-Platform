from fastapi import APIRouter
from pydantic import BaseModel

from app.services.adk_runner import run_planner

router = APIRouter()


class AnalyzeRequest(BaseModel):
    query: str


@router.post("/analyze")
async def analyze(request: AnalyzeRequest):

    answer = await run_planner(request.query)

    return {
        "response": answer
    }