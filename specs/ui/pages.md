# UI Pages & Components

## Phase II — Full-Stack Web Application

## Tech
- Next.js 16+ with App Router
- Responsive design (mobile + desktop)

## Pages

### /auth/signin — Sign In Page
- Email and password fields
- Sign in button
- Link to signup page
- Show error message if credentials wrong

### /auth/signup — Sign Up Page
- Name, email and password fields
- Sign up button
- Link to signin page
- Show error message if email taken

### / — Dashboard (protected)
- Redirect to /auth/signin if not logged in
- Show all tasks for logged-in user
- Add task form at the top
- Task list below the form
- Sign out button

## Components

### TaskForm
- Title input (required)
- Description input (optional)
- Submit button

### TaskCard
- Shows task title, description, status
- Complete/incomplete toggle button
- Edit button
- Delete button

### TaskList
- Renders list of TaskCards
- Shows "No tasks yet" if empty