from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class ExecutionState(str, Enum):
    INITIALIZED = "initialized"

    PLANNING = "planning"

    RESEARCHING = "researching"

    VERIFYING = "verifying"

    REPORTING = "reporting"

    COMPLETED = "completed"

    FAILED = "failed"


class ExecutionEventType(str, Enum):
    SESSION_STARTED = "session_started"

    PLANNER_STARTED = "planner_started"
    PLANNER_COMPLETED = "planner_completed"

    RESEARCH_STARTED = "research_started"
    RESEARCH_COMPLETED = "research_completed"

    VERIFIER_STARTED = "verifier_started"
    VERIFIER_COMPLETED = "verifier_completed"

    REPORTER_STARTED = "reporter_started"
    REPORTER_COMPLETED = "reporter_completed"

    EXECUTION_COMPLETED = "execution_completed"

    EXECUTION_FAILED = "execution_failed"


class ExecutionEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))

    type: ExecutionEventType

    timestamp: datetime = Field(default_factory=datetime.utcnow)

    state: ExecutionState

    agent: str | None = None

    message: str | None = None

    metadata: dict = Field(default_factory=dict)


class ExecutionContext(BaseModel):
    execution_id: str = Field(default_factory=lambda: str(uuid4()))

    state: ExecutionState = ExecutionState.INITIALIZED

    current_agent: str | None = None

    previous_agent: str | None = None

    iteration: int = 0

    max_iterations: int = 5

    started_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)

    completed: bool = False

    failed: bool = False

    last_error: str | None = None

    events: list[ExecutionEvent] = Field(default_factory=list)