from datetime import datetime

from app.schemas import (
    Evidence,
    Finding,
    Report,
    ResearchPlan,
)
from app.workspace.status import WorkspaceStatus
from app.workspace.workspace import Workspace


class WorkspaceManager:
    _workspaces: dict[str, Workspace] = {}

    @classmethod
    def create(cls, user_query: str) -> Workspace:
        workspace = Workspace(user_query=user_query)
        cls._workspaces[workspace.id] = workspace
        return workspace

    @classmethod
    def get(cls, workspace_id: str) -> Workspace | None:
        return cls._workspaces.get(workspace_id)

    @classmethod
    def update_status(
        cls,
        workspace_id: str,
        status: WorkspaceStatus,
    ) -> Workspace | None:
        workspace = cls.get(workspace_id)

        if workspace is None:
            return None

        workspace.status = status
        workspace.updated_at = datetime.utcnow()

        return workspace

    @classmethod
    def set_research_plan(
        cls,
        workspace_id: str,
        research_plan: ResearchPlan,
    ) -> Workspace | None:
        workspace = cls.get(workspace_id)

        if workspace is None:
            return None

        workspace.research_plan = research_plan
        workspace.updated_at = datetime.utcnow()

        return workspace

    @classmethod
    def add_evidence(
        cls,
        workspace_id: str,
        evidence: Evidence,
    ) -> Workspace | None:
        workspace = cls.get(workspace_id)

        if workspace is None:
            return None

        workspace.evidence.append(evidence)
        workspace.updated_at = datetime.utcnow()

        return workspace

    @classmethod
    def add_finding(
        cls,
        workspace_id: str,
        finding: Finding,
    ) -> Workspace | None:
        workspace = cls.get(workspace_id)

        if workspace is None:
            return None

        workspace.findings.append(finding)
        workspace.updated_at = datetime.utcnow()

        return workspace

    @classmethod
    def set_report(
        cls,
        workspace_id: str,
        report: Report,
    ) -> Workspace | None:
        workspace = cls.get(workspace_id)

        if workspace is None:
            return None

        workspace.report = report
        workspace.updated_at = datetime.utcnow()

        return workspace

    @classmethod
    def delete(cls, workspace_id: str):
        cls._workspaces.pop(workspace_id, None)