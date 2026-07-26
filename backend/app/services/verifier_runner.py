import json
import uuid

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agents.verifier import verifier_agent
from app.schemas import Evidence


APP_NAME = "arip"

session_service = InMemorySessionService()

runner = Runner(
    agent=verifier_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


async def run_verifier_agent(evidence: list[Evidence]) -> str:
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
Analyze the following research evidence and produce verified findings.

Evidence:
{json.dumps([item.model_dump() for item in evidence], indent=2)}

Return ONLY valid JSON.
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