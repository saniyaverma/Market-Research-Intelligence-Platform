from enum import Enum


class WorkspaceStatus(str, Enum):
    CREATED = "created"

    ACTIVE = "active"

    COMPLETED = "completed"

    FAILED = "failed"

    ARCHIVED = "archived"