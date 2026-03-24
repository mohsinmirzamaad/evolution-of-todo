from pathlib import Path

from agents import Agent, Runner
from agents.mcp.server import MCPServerStdio

BACKEND_DIR = str(Path(__file__).resolve().parent.parent)


def _create_mcp_server() -> MCPServerStdio:
    return MCPServerStdio(
        params={
            "command": "uv",
            "args": ["run", "mcp", "run", "todo_mcp/server.py:mcp_server"],
        },
        cwd=BACKEND_DIR,
    )


def _create_agent(user_id: str, mcp_server: MCPServerStdio) -> Agent:
    return Agent(
        name="Todo Assistant",
        instructions=(
            f"You are a helpful todo list assistant. The current user's ID is: {user_id}. "
            "Always use this user_id when calling any tool.\n\n"
            "You can add, list, complete, delete, and update tasks using the available tools.\n"
            "After performing an action, confirm what you did in a friendly way.\n"
            "When listing tasks, format them nicely.\n"
            "If a task is not found, let the user know kindly.\n"
            "Never make up task IDs — list tasks first if you need an ID."
        ),
        mcp_servers=[mcp_server],
    )


async def run_agent(user_id: str, messages: list[dict]) -> tuple[str, list[dict]]:
    """Run the agent with conversation history.

    Args:
        user_id: The authenticated user's ID.
        messages: List of {"role": "user"/"assistant", "content": "..."} dicts.

    Returns:
        Tuple of (response_text, tool_calls_list).
    """
    mcp_server = _create_mcp_server()
    agent = _create_agent(user_id, mcp_server)

    async with mcp_server:
        result = await Runner.run(agent, input=messages)

    tool_calls = []
    for item in result.new_items:
        if hasattr(item, "raw_item") and hasattr(item.raw_item, "type"):
            if item.raw_item.type == "function_call":
                tool_calls.append({
                    "tool_name": item.raw_item.name,
                    "arguments": item.raw_item.arguments,
                })

    return result.final_output, tool_calls
