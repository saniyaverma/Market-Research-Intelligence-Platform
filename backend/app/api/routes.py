from fastapi import APIRouter
from pydantic import BaseModel

from app.workspace import WorkspaceManager
from app.workflows import RootOrchestrator

router = APIRouter()


class AnalyzeRequest(BaseModel):
    query: str


@router.post("/analyze")
async def analyze(request: AnalyzeRequest):

    workspace = WorkspaceManager.create(
        request.query
    )

    orchestrator = RootOrchestrator()

    workspace = await orchestrator.run(
        workspace.id
    )

    return workspace.model_dump()