import uuid

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agents.research import research_agent
from app.schemas import ResearchTask

APP_NAME = "arip"

session_service = InMemorySessionService()

runner = Runner(
    agent=research_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


async def run_research_agent(task: ResearchTask) -> str:
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
Research the following task.

Task ID:
{task.id}

Title:
{task.title}

Description:
{task.description}

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