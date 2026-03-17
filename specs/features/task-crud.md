# Feature: Task CRUD Operations

## Phase I — In-Memory Console App

## User Stories
- As a user, I can add a new task with a title and description
- As a user, I can view all my tasks with their status
- As a user, I can update a task's title or description
- As a user, I can delete a task by its ID
- As a user, I can mark a task as complete or incomplete

## Acceptance Criteria

### Add Task
- Title is required
- Description is optional
- Each task gets a unique auto-incremented ID
- New task is incomplete by default

### View Tasks
- Display ID, title, description, status (complete/incomplete)
- Show message if no tasks exist

### Update Task
- Find task by ID
- Allow updating title and/or description
- Show error if task ID not found

### Delete Task
- Remove task by ID
- Show error if task ID not found

### Mark Complete
- Toggle between complete and incomplete
- Show error if task ID not found

## Data Model
- id: integer (auto-incremented)
- title: string (required)
- description: string (optional, default empty)
- completed: boolean (default False)