# API Endpoints

## Phase II — Full-Stack Web Application

## Base URL
- Development: http://localhost:8000
- Production: (Vercel backend URL)

## Authentication
All endpoints require JWT token in header:
Authorization: Bearer <token>

## Task Endpoints

### GET /api/{user_id}/tasks
- List all tasks for authenticated user
- Query params: status (all/pending/completed)
- Response: array of task objects

### POST /api/{user_id}/tasks
- Create a new task
- Body: title (required), description (optional)
- Response: created task object

### GET /api/{user_id}/tasks/{id}
- Get single task by ID
- Response: task object

### PUT /api/{user_id}/tasks/{id}
- Update task title or description
- Body: title (optional), description (optional)
- Response: updated task object

### DELETE /api/{user_id}/tasks/{id}
- Delete task by ID
- Response: success message

### PATCH /api/{user_id}/tasks/{id}/complete
- Toggle task completion status
- Response: updated task object

## Error Responses
- 401 Unauthorized — missing or invalid JWT token
- 404 Not Found — task ID does not exist
- 422 Validation Error — invalid request body