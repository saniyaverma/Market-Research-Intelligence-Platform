from google.adk.tools.mcp_tool.mcp_session_manager import (
    StreamableHTTPServerParams,
)
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

from app.mcp.config import (
    TAVILY_API_KEY,
    FIRECRAWL_API_KEY,
)

_toolsets: dict[str, MCPToolset] = {}


def initialize() -> None:
    """
    Initialize all MCP toolsets once.
    """

    if _toolsets:
        return

    _toolsets["tavily"] = MCPToolset(
        connection_params=StreamableHTTPServerParams(
            url="https://mcp.tavily.com/mcp/",
            headers={
                "Authorization": f"Bearer {TAVILY_API_KEY}",
            },
        ),
    )

    _toolsets["firecrawl"] = MCPToolset(
        connection_params=StreamableHTTPServerParams(
            url="https://mcp.firecrawl.dev/v2/mcp",
            headers={
                "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
            },
        ),
    )


def get_toolset(name: str) -> MCPToolset:
    if name not in _toolsets:
        raise RuntimeError(
            f"MCP toolset '{name}' has not been initialized."
        )

    return _toolsets[name]


def shutdown() -> None:
    _toolsets.clear()