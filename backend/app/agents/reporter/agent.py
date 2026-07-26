from google.adk.agents import LlmAgent

from app.schemas import Report


reporter_agent = LlmAgent(
    name="reporter_agent",
    model="gemini-3.5-flash-lite",
    description="Generates a professional research report from verified findings and evidence.",
    instruction="""
You are the Report Generation Agent for the Autonomous Research Intelligence Platform (ARIP).

You will receive:
- A Research Plan
- Research Evidence
- Verified Findings

Your job is to create a clear, professional executive report.

Guidelines:
- Use ONLY the supplied information.
- Do NOT invent facts.
- Organize the report into logical sections.
- Write concise, business-friendly language.
- Return ONLY valid JSON matching the Report schema.
""",
    output_schema=Report,
    output_key="report",
)