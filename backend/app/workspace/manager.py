from datetime import datetime

from app.schemas import (
    Evidence,
    Finding,
    Report,
    ResearchPlan,
)
from app.workspace.execution import (
    ExecutionEventType,
    ExecutionState,
)
from app.workspace.event_logger import WorkspaceEventLogger
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
    def delete(cls, workspace_id: str):
        cls._workspaces.pop(workspace_id, None)

    # ------------------------------------------------------------------
    # Workspace Lifecycle
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Execution Context
    # ------------------------------------------------------------------

    @classmethod
    def set_execution_state(
        cls,
        workspace_id: str,
        state: ExecutionState,
        current_agent: str | None = None,
    ) -> Workspace | None:

        workspace = cls.get(workspace_id)

        if workspace is None:
            return None

        workspace.execution.previous_agent = (
            workspace.execution.current_agent
        )

        workspace.execution.current_agent = current_agent
        workspace.execution.state = state
        workspace.execution.updated_at = datetime.utcnow()

        return workspace

    @classmethod
    def increment_iteration(
        cls,
        workspace_id: str,
    ) -> Workspace | None:

        workspace = cls.get(workspace_id)

        if workspace is None:
            return None

        workspace.execution.iteration += 1
        workspace.execution.updated_at = datetime.utcnow()

        return workspace

    @classmethod
    def add_execution_event(
        cls,
        workspace_id: str,
        event: ExecutionEventType,
        state: ExecutionState,
        agent: str | None = None,
        message: str | None = None,
        metadata: dict | None = None,
    ) -> Workspace | None:

        workspace = cls.get(workspace_id)

        if workspace is None:
            return None

        WorkspaceEventLogger.log(
            workspace=workspace,
            event=event,
            state=state,
            agent=agent,
            message=message,
            metadata=metadata,
        )

        return workspace

    @classmethod
    def mark_completed(
        cls,
        workspace_id: str,
    ) -> Workspace | None:

        workspace = cls.get(workspace_id)

        if workspace is None:
            return None

        workspace.execution.completed = True
        workspace.execution.state = ExecutionState.COMPLETED
        workspace.updated_at = datetime.utcnow()

        return workspace

    @classmethod
    def mark_failed(
        cls,
        workspace_id: str,
        error: str,
    ) -> Workspace | None:

        workspace = cls.get(workspace_id)

        if workspace is None:
            return None

        workspace.execution.failed = True
        workspace.execution.last_error = error
        workspace.execution.state = ExecutionState.FAILED
        workspace.updated_at = datetime.utcnow()

        return workspace

    # ------------------------------------------------------------------
    # Research Data
    # ------------------------------------------------------------------

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