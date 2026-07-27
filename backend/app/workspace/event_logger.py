from datetime import datetime

from app.core.logger import execution_logger
from app.workspace.execution import (
    ExecutionEvent,
    ExecutionEventType,
    ExecutionState,
)
from app.workspace.workspace import Workspace


class WorkspaceEventLogger:

    @staticmethod
    def log(
        workspace: Workspace,
        event: ExecutionEventType,
        state: ExecutionState,
        agent: str | None = None,
        message: str | None = None,
        metadata: dict | None = None,
    ):

        execution_event = ExecutionEvent(
            type=event,
            state=state,
            agent=agent,
            message=message,
            metadata=metadata or {},
        )

        workspace.execution.events.append(
            execution_event
        )

        workspace.execution.updated_at = datetime.utcnow()

        execution_logger.info(
            f"[{state}] {event}"
        )