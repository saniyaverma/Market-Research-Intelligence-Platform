from app.schemas import (
    Evidence,
    Finding,
    Report,
    ResearchPlan,
    ResearchTask,
)
from app.workspace import (
    WorkspaceManager,
    WorkspaceStatus,
)


def get_workspace(workspace_id: str):
    """
    Retrieve a workspace.
    """
    return WorkspaceManager.get(workspace_id)


def update_workspace_status(
    workspace_id: str,
    status: WorkspaceStatus,
):
    """
    Update workspace status.
    """
    return WorkspaceManager.update_status(
        workspace_id,
        status,
    )


def set_research_plan(
    workspace_id: str,
    research_plan: ResearchPlan,
):
    """
    Store the generated research plan.
    """
    return WorkspaceManager.set_research_plan(
        workspace_id,
        research_plan,
    )


def add_evidence(
    workspace_id: str,
    evidence: Evidence,
):
    """
    Store one evidence item.
    """
    return WorkspaceManager.add_evidence(
        workspace_id,
        evidence,
    )


def add_finding(
    workspace_id: str,
    finding: Finding,
):
    """
    Store one verified finding.
    """
    return WorkspaceManager.add_finding(
        workspace_id,
        finding,
    )


def set_report(
    workspace_id: str,
    report: Report,
):
    """
    Store the final report.
    """
    return WorkspaceManager.set_report(
        workspace_id,
        report,
    )


def get_pending_tasks(
    workspace_id: str,
) -> list[ResearchTask]:
    """
    Return all pending research tasks.
    """
    workspace = WorkspaceManager.get(workspace_id)

    if (
        workspace is None
        or workspace.research_plan is None
    ):
        return []

    return [
        task
        for task in workspace.research_plan.tasks
        if task.status == "pending"
    ]