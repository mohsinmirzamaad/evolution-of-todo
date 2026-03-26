from collections.abc import AsyncIterator

from agents import Runner
from chatkit.agents import AgentContext, simple_to_agent_input, stream_agent_response
from chatkit.server import ChatKitServer
from chatkit.types import ThreadMetadata, ThreadStreamEvent, UserMessageItem

from agent.agent import _create_agent, _create_mcp_server
from app.chatkit_store import PostgresStore, RequestContext


class TodoChatKitServer(ChatKitServer["RequestContext"]):
    async def respond(
        self,
        thread: ThreadMetadata,
        input_user_message: UserMessageItem | None,
        context: "RequestContext",
    ) -> AsyncIterator[ThreadStreamEvent]:
        items_page = await self.store.load_thread_items(
            thread.id, after=None, limit=50, order="asc", context=context
        )
        items = items_page.data
        input_items = simple_to_agent_input(items)

        agent_context = AgentContext(
            thread=thread,
            store=self.store,
            request_context=context,
        )

        mcp_server = _create_mcp_server()
        agent = _create_agent(context.user_id, mcp_server)

        async with mcp_server:
            result = Runner.run_streamed(agent, input=input_items)
            async for event in stream_agent_response(agent_context, result):
                yield event


def create_chatkit_server() -> TodoChatKitServer:
    store = PostgresStore()
    return TodoChatKitServer(store=store)
