from enum import Enum


class WorkspaceStatus(str, Enum):
    CREATED = "created"

    PLANNING = "planning"
    PLANNED = "planned"

    RESEARCHING = "researching"
    RESEARCHED = "researched"

    REPORTING = "reporting"
    COMPLETED = "completed"

    FAILED = "failed"