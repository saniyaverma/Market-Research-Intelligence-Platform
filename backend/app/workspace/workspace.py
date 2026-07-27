from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from app.schemas import (
    ResearchPlan,
    Evidence,
    Finding,
    Report,
)
from app.workspace.status import WorkspaceStatus
from app.workspace.execution import ExecutionContext


class Workspace(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))

    # User input
    user_query: str

    # Workspace lifecycle
    status: WorkspaceStatus = WorkspaceStatus.CREATED

    execution: ExecutionContext = Field(default_factory=ExecutionContext)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Shared state
    research_plan: ResearchPlan | None = None
    evidence: list[Evidence] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)
    report: Report | None = None

    # Extra runtime information
    metadata: dict = Field(default_factory=dict)