# Todo App - Hackathon II

## Project Overview
This is a monorepo using Spec-Kit Plus for spec-driven development.
Built for Panaversity AI Agent Factory Hackathon II.

## Spec-Kit Structure
- /specs/overview.md - Project overview
- /specs/features/task-crud.md - Task CRUD feature spec
- /specs/features/authentication.md - Auth feature spec
- /specs/features/chatbot.md - AI chatbot feature spec (Phase III)
- /specs/api/rest-endpoints.md - API endpoints spec
- /specs/database/schema.md - Database schema spec
- /specs/ui/pages.md - UI pages and components spec
- .spec-kit/config.yaml - Spec-Kit configuration

## Project Structure
- /phase1/src - Phase I Python console app
- /frontend - Phase II Next.js app
- /backend - Phase II FastAPI app
- /backend/mcp - Phase III MCP server (tools for AI agent)
- /backend/agent - Phase III OpenAI Agents SDK integration
- /backend/models - Database models (conversations, messages)

## Phase III — AI-Powered Chatbot
- Users manage todos via natural language conversation
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK exposing tools (add_task, list_tasks, complete_task, delete_task, update_task)
- Chat UI: OpenAI ChatKit on frontend
- Chat API: POST /api/{user_id}/chat
- Database: Conversation and Message models in Neon PostgreSQL
- Agent uses MCP tools to perform CRUD operations on tasks
- Conversation history persisted per user

## Development Rules
1. Use Python 3.13+ for backend
2. Use uv for Python package management
3. Use Next.js 16+ App Router for frontend
4. Follow clean code principles
5. No manual code — implement from specs only
6. Always read specs before implementing
7. Use OpenAI Agents SDK for Phase III AI agent
8. Use official MCP SDK for Phase III MCP server
9. All chat endpoints require valid JWT token (same auth as Phase II)