# Feature: Advanced Todo Features

## Phase V — Advanced Cloud Deployment

## Part A: Advanced Features

### Intermediate Level
- Priorities — assign high/medium/low to tasks
- Tags/Categories — label tasks (work/home/personal)
- Search — search tasks by keyword
- Filter — filter by status, priority, tag, date
- Sort — sort by due date, priority, alphabetically

### Advanced Level
- Due Dates — set deadline with date/time
- Recurring Tasks — auto-reschedule repeating tasks
- Reminders — browser notifications for due tasks

## Event-Driven Architecture (Kafka)
- task-events topic — publish on every task operation
- reminders topic — publish when task due date approaches
- Notification service consumes reminders topic

## Dapr Components
- pubsub.kafka — event streaming
- state.postgresql — conversation state
- bindings.cron — trigger reminder checks
- secretstores.kubernetes — API keys, DB credentials

## Database Changes
- tasks table: add priority, tags, due_date, recurring fields
- notifications table: track sent reminders