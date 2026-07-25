import json

from fastapi import APIRouter
from pydantic import BaseModel

from app.schemas import ResearchPlan
from app.services.adk_runner import run_root_agent
from app.workspace import WorkspaceManager, WorkspaceStatus

router = APIRouter()


class AnalyzeRequest(BaseModel):
    query: str


@router.post("/analyze")
async def analyze(request: AnalyzeRequest):
    # Create a new workspace
    workspace = WorkspaceManager.create(request.query)

    # Update workspace status: Planning started
    WorkspaceManager.update_status(
        workspace.id,
        WorkspaceStatus.PLANNING,
    )

    # Run the planner agent
    planner_output = await run_root_agent(request.query)

    # Convert planner JSON string to Python dictionary
    planner_data = json.loads(planner_output)

    # Validate against our schema
    research_plan = ResearchPlan.model_validate(planner_data)

    # Store the validated research plan via the WorkspaceManager
    WorkspaceManager.set_research_plan(
        workspace.id,
        research_plan,
    )

    # Update workspace status: Planning completed
    WorkspaceManager.update_status(
        workspace.id,
        WorkspaceStatus.PLANNED,
    )

    # Fetch the latest workspace state
    workspace = WorkspaceManager.get(workspace.id)

    return workspace.model_dump()