# Feature: AI Todo Chatbot

## Phase III — AI-Powered Chatbot

## Objective
Allow users to manage their todo list through natural language
conversation using OpenAI Agents SDK and MCP tools.

## Tech Stack
- Frontend: OpenAI ChatKit
- Backend: Python FastAPI
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- Database: Neon PostgreSQL (conversations + messages)

## MCP Tools
The MCP server exposes these tools to the AI agent:

### add_task
- Parameters: user_id (required), title (required), description (optional)
- Returns: task_id, status, title

### list_tasks
- Parameters: user_id (required), status (optional: all/pending/completed)
- Returns: array of task objects

### complete_task
- Parameters: user_id (required), task_id (required)
- Returns: task_id, status, title

### delete_task
- Parameters: user_id (required), task_id (required)
- Returns: task_id, status, title

### update_task
- Parameters: user_id (required), task_id (required), title (optional), description (optional)
- Returns: task_id, status, title

## Chat API Endpoint
POST /api/{user_id}/chat
- Request: conversation_id (optional), message (required)
- Response: conversation_id, response, tool_calls

## Database Models
- Conversation: id, user_id, created_at, updated_at
- Message: id, user_id, conversation_id, role, content, created_at

## Agent Behavior
- Add task when user says: add, create, remember
- List tasks when user says: show, list, what
- Complete task when user says: done, complete, finished
- Delete task when user says: delete, remove, cancel
- Update task when user says: change, update, rename
- Always confirm actions with friendly response
- Handle errors gracefully

## Conversation Flow
1. Receive user message
2. Fetch conversation history from database
3. Store user message in database
4. Run agent with MCP tools
5. Store assistant response in database
6. R