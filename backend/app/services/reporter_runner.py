import json
import uuid

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agents.reporter import reporter_agent
from app.workspace.workspace import Workspace


APP_NAME = "arip"

session_service = InMemorySessionService()

runner = Runner(
    agent=reporter_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


async def run_reporter_agent(workspace: Workspace) -> str:
    user_id = "local-user"
    session_id = str(uuid.uuid4())

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=f"""
Generate a professional research report using the following information.

Research Plan:
{json.dumps(workspace.research_plan.model_dump(), indent=2)}

Evidence:
{json.dumps([e.model_dump() for e in workspace.evidence], indent=2)}

Verified Findings:
{json.dumps([f.model_dump() for f in workspace.findings], indent=2)}

Return ONLY valid JSON matching the Report schema.
Do not use markdown.
Do not add explanations.
"""
            )
        ],
    )

    response = ""

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message,
    ):
        if (
            event.is_final_response()
            and event.content
            and event.content.parts
        ):
            response = "".join(
                part.text or ""
                for part in event.content.parts
            )

    return response