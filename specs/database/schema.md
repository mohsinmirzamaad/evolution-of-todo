# Database Schema

## Phase II — Full-Stack Web Application

## Database
- Neon Serverless PostgreSQL
- ORM: SQLModel

## Tables

### users (managed by Better Auth)
- id: string (primary key)
- email: string (unique)
- name: string
- created_at: timestamp

### tasks
- id: integer (primary key, auto-incremented)
- user_id: string (foreign key → users.id)
- title: string (required, max 200 chars)
- description: text (optional, max 1000 chars)
- completed: boolean (default False)
- created_at: timestamp
- updated_at: timestamp

## Indexes
- tasks.user_id — for filtering tasks by user
- tasks.completed — for filtering by status

## Rules
- A task always belongs to one user
- Deleting a user deletes all their tasks
- user_id is always set from JWT token, never from request body