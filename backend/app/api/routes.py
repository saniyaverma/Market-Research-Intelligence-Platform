import json

from fastapi import APIRouter
from pydantic import BaseModel

from app.schemas import ResearchPlan
from app.services.planner_runner import run_planner_agent
from app.workspace import WorkspaceManager, WorkspaceStatus
from app.workflows import ResearchWorkflow

router = APIRouter()


class AnalyzeRequest(BaseModel):
    query: str


@router.post("/analyze")
async def analyze(request: AnalyzeRequest):

    workspace = WorkspaceManager.create(request.query)

    WorkspaceManager.update_status(
        workspace.id,
        WorkspaceStatus.PLANNING,
    )

    planner_output = await run_planner_agent(request.query)

    planner_data = json.loads(planner_output)

    research_plan = ResearchPlan.model_validate(
        planner_data
    )

    WorkspaceManager.set_research_plan(
        workspace.id,
        research_plan,
    )

    WorkspaceManager.update_status(
        workspace.id,
        WorkspaceStatus.PLANNED,
    )

    workflow = ResearchWorkflow()

    await workflow.execute(workspace.id)

    workspace = WorkspaceManager.get(workspace.id)

    return workspace.model_dump()