import json

from app.schemas import (
    Evidence,
    Findings,
    Report,
    ResearchPlan,
)
from app.services.planner_runner import run_planner_agent
from app.services.research_runner import run_research_agent
from app.services.reporter_runner import run_reporter_agent
from app.services.verifier_runner import run_verifier_agent
from app.workspace import WorkspaceManager, WorkspaceStatus
from app.workspace.execution import (
    ExecutionEventType,
    ExecutionState,
)


class RootOrchestrator:
    """
    Root execution engine for ARIP.

    Responsibilities:
    - Control execution flow
    - Maintain execution state
    - Emit execution events
    - Invoke specialized agents
    - Update Workspace
    """

    async def run(self, workspace_id: str):

        workspace = WorkspaceManager.get(workspace_id)

        if workspace is None:
            raise ValueError("Workspace not found")

        try:

            # ==========================================================
            # SESSION START
            # ==========================================================

            WorkspaceManager.update_status(
                workspace_id,
                WorkspaceStatus.ACTIVE,
            )

            WorkspaceManager.set_execution_state(
                workspace_id,
                ExecutionState.INITIALIZED,
            )

            WorkspaceManager.add_execution_event(
                workspace_id,
                ExecutionEventType.SESSION_STARTED,
                ExecutionState.INITIALIZED,
                message="Research session started.",
            )

            # ==========================================================
            # PLANNING
            # ==========================================================

            WorkspaceManager.set_execution_state(
                workspace_id,
                ExecutionState.PLANNING,
                current_agent="planner_agent",
            )

            WorkspaceManager.add_execution_event(
                workspace_id,
                ExecutionEventType.PLANNER_STARTED,
                ExecutionState.PLANNING,
                agent="planner_agent",
            )

            planner_response = await run_planner_agent(
                workspace.user_query
            )

            planner_data = json.loads(planner_response)

            research_plan = ResearchPlan.model_validate(
                planner_data
            )

            WorkspaceManager.set_research_plan(
                workspace_id,
                research_plan,
            )

            WorkspaceManager.add_execution_event(
                workspace_id,
                ExecutionEventType.PLANNER_COMPLETED,
                ExecutionState.PLANNING,
                agent="planner_agent",
            )

            workspace = WorkspaceManager.get(workspace_id)

            # ==========================================================
            # RESEARCH
            # ==========================================================

            WorkspaceManager.set_execution_state(
                workspace_id,
                ExecutionState.RESEARCHING,
                current_agent="research_agent",
            )

            WorkspaceManager.add_execution_event(
                workspace_id,
                ExecutionEventType.RESEARCH_STARTED,
                ExecutionState.RESEARCHING,
                agent="research_agent",
            )

            for task in workspace.research_plan.tasks:

                WorkspaceManager.increment_iteration(
                    workspace_id
                )

                response = await run_research_agent(task)

                evidence_data = json.loads(response)

                evidence = Evidence.model_validate(
                    evidence_data
                )

                WorkspaceManager.add_evidence(
                    workspace_id,
                    evidence,
                )

            WorkspaceManager.add_execution_event(
                workspace_id,
                ExecutionEventType.RESEARCH_COMPLETED,
                ExecutionState.RESEARCHING,
                agent="research_agent",
            )

            workspace = WorkspaceManager.get(workspace_id)

            # ==========================================================
            # VERIFICATION
            # ==========================================================

            WorkspaceManager.set_execution_state(
                workspace_id,
                ExecutionState.VERIFYING,
                current_agent="verifier_agent",
            )

            WorkspaceManager.add_execution_event(
                workspace_id,
                ExecutionEventType.VERIFIER_STARTED,
                ExecutionState.VERIFYING,
                agent="verifier_agent",
            )

            verifier_response = await run_verifier_agent(
                workspace.evidence
            )

            findings_data = json.loads(verifier_response)

            findings = Findings.model_validate(
                findings_data
            )

            for finding in findings.findings:

                WorkspaceManager.add_finding(
                    workspace_id,
                    finding,
                )

            WorkspaceManager.add_execution_event(
                workspace_id,
                ExecutionEventType.VERIFIER_COMPLETED,
                ExecutionState.VERIFYING,
                agent="verifier_agent",
            )

            workspace = WorkspaceManager.get(workspace_id)

            # ==========================================================
            # REPORTING
            # ==========================================================

            WorkspaceManager.set_execution_state(
                workspace_id,
                ExecutionState.REPORTING,
                current_agent="reporter_agent",
            )

            WorkspaceManager.add_execution_event(
                workspace_id,
                ExecutionEventType.REPORTER_STARTED,
                ExecutionState.REPORTING,
                agent="reporter_agent",
            )

            reporter_response = await run_reporter_agent(
                workspace
            )

            report_data = json.loads(reporter_response)

            report = Report.model_validate(report_data)

            WorkspaceManager.set_report(
                workspace_id,
                report,
            )

            WorkspaceManager.add_execution_event(
                workspace_id,
                ExecutionEventType.REPORTER_COMPLETED,
                ExecutionState.REPORTING,
                agent="reporter_agent",
            )

            # ==========================================================
            # COMPLETE
            # ==========================================================

            WorkspaceManager.mark_completed(
                workspace_id
            )

            WorkspaceManager.update_status(
                workspace_id,
                WorkspaceStatus.COMPLETED,
            )

            WorkspaceManager.add_execution_event(
                workspace_id,
                ExecutionEventType.EXECUTION_COMPLETED,
                ExecutionState.COMPLETED,
            )

            return WorkspaceManager.get(
                workspace_id
            )

        except Exception as e:

            WorkspaceManager.mark_failed(
                workspace_id,
                str(e),
            )

            WorkspaceManager.update_status(
                workspace_id,
                WorkspaceStatus.FAILED,
            )

            WorkspaceManager.add_execution_event(
                workspace_id,
                ExecutionEventType.EXECUTION_FAILED,
                ExecutionState.FAILED,
                message=str(e),
            )

            raise