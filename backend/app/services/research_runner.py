import uuid

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agents.research import create_research_agent
from app.mcp.manager import initialize
from app.schemas import ResearchTask

APP_NAME = "arip"

session_service = InMemorySessionService()

_runner: Runner | None = None


def get_runner() -> Runner:
    """
    Lazily create the Research Runner.

    The first time this function is called:
        1. Initialize all MCP toolsets.
        2. Create the Research Agent.
        3. Create the ADK Runner.

    Subsequent calls reuse the same Runner instance.
    """

    global _runner

    if _runner is None:
        initialize()

        research_agent = create_research_agent()

        _runner = Runner(
            agent=research_agent,
            app_name=APP_NAME,
            session_service=session_service,
        )

    return _runner


async def run_research_agent(task: ResearchTask) -> str:
    """
    Execute a research task using the singleton Research Runner.
    """

    runner = get_runner()

    user_id = "local-user"
    session_id = str(uuid.uuid4())

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )

    prompt = f"""
Research the following task and produce structured evidence.

Task ID:
{task.id}

Title:
{task.title}

Description:
{task.description}

Instructions:

- Decide which research tool(s) are most appropriate.
- Use the available research tools whenever external information is required.
- Search, scrape, crawl, or retrieve webpages as needed.
- Prefer primary and authoritative sources.
- Cross-check important facts whenever possible.
- Return ONLY valid JSON matching the required schema.
- Do NOT use markdown.
- Do NOT explain your reasoning.
"""

    message = types.Content(
        role="user",
        parts=[
            types.Part(text=prompt)
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