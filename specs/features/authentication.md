# Feature: Authentication

## Phase II — Full-Stack Web Application

## User Stories
- As a user, I can sign up with email and password
- As a user, I can sign in with email and password
- As a user, I can sign out
- As a user, I can only see my own tasks

## Tech
- Better Auth on Next.js frontend
- JWT tokens passed to FastAPI backend
- Shared secret key between frontend and backend

## Acceptance Criteria

### Sign Up
- Email and password required
- Email must be unique
- Password minimum 8 characters
- Redirect to dashboard after signup

### Sign In
- Email and password required
- Show error if credentials wrong
- Redirect to dashboard after signin

### Sign Out
- Clear session and redirect to login page

### Task Ownership
- Every task is linked to the logged-in user
- Users cannot see or modify other users tasks
- All API requests require valid JWT token
- Return 401 if token missing or invalid