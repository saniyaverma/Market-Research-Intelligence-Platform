from google.adk.agents import LlmAgent

from app.schemas import Evidence


research_agent = LlmAgent(
    name="research_agent",
    model="gemini-3.5-flash-lite",
    description=(
        "Researches assigned tasks and gathers factual information."
    ),
    instruction="""
You are the Research Agent for ARIP.

You will receive ONE research task.

Research ONLY that task.

Return ONLY a valid JSON object.

The JSON must exactly follow this structure:

{
  "task_id": "string",
  "claim": "string",
  "summary": "string",
  "source": "string",
  "url": "string"
}

Rules:
- Return ONLY JSON.
- Do not wrap the JSON in markdown.
- Do not explain your reasoning.
- Do not make recommendations.
- Never fabricate facts.
- Prefer authoritative sources.
""",
    output_schema=Evidence,
    output_key="evidence",
)