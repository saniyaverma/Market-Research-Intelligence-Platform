import json

from app.schemas import Evidence
from app.services.research_runner import run_research_agent
from app.workspace import WorkspaceManager


class ResearchWorkflow:

    async def execute(self, workspace_id: str):

        workspace = WorkspaceManager.get(workspace_id)

        if workspace is None:
            raise ValueError("Workspace not found")

        if workspace.research_plan is None:
            raise ValueError("Research plan not found")

        for task in workspace.research_plan.tasks:

            response = await run_research_agent(task)

            evidence_data = json.loads(response)

            evidence = Evidence.model_validate(evidence_data)

            WorkspaceManager.add_evidence(
                workspace.id,
                evidence,
            )

        return WorkspaceManager.get(workspace.id)