import json

from app.schemas import Evidence, Findings
from app.services.research_runner import run_research_agent
from app.services.verifier_runner import run_verifier_agent
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

        # Refresh workspace to get all collected evidence
        workspace = WorkspaceManager.get(workspace.id)

        verifier_response = await run_verifier_agent(
            workspace.evidence
        )

        findings_data = json.loads(verifier_response)

        findings = Findings.model_validate(findings_data)

        for finding in findings.findings:
            WorkspaceManager.add_finding(
                workspace.id,
                finding,
            )

        return WorkspaceManager.get(workspace.id)