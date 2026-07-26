from app.tools.workspace import (
    add_evidence,
    add_finding,
    get_pending_tasks,
    get_workspace,
    set_report,
    set_research_plan,
    update_workspace_status,
)

# ------------------------------------------------------------------
# Workspace Tools
# ------------------------------------------------------------------

WORKSPACE_TOOLS = [
    get_workspace,
    update_workspace_status,
    set_research_plan,
    add_evidence,
    add_finding,
    set_report,
    get_pending_tasks,
]

# ------------------------------------------------------------------
# Master Tool Registry
# ------------------------------------------------------------------

ALL_TOOLS = [
    *WORKSPACE_TOOLS,
]