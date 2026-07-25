from google.adk.agents import LlmAgent

from app.agents.planner import planner_agent


root_agent = LlmAgent(
    name="root_agent",
    model="gemini-3.5-flash-lite",
    description="Root orchestrator for the ARIP Market Research Intelligence Platform.",
    instruction="""
You are the Root Agent for ARIP.

Your responsibility is to understand the user's request and delegate work
to the appropriate specialist agent.

Do not perform research yourself.
Do not fabricate information.
Coordinate the workflow using your available sub-agents.
""",
    sub_agents=[
        planner_agent,
    ],
)