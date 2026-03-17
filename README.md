# Evolution of Todo

> A Todo application that evolves across 5 phases — from a simple Python console app to a cloud-native AI-powered distributed system.

**Panaversity AI Agent Factory Hackathon II** | Spec-driven development with Claude Code + Spec-Kit Plus

---

## Project Overview

This monorepo demonstrates how a single application can evolve in complexity, architecture, and capability across multiple phases. Each phase builds on the previous one, introducing new layers of the stack while keeping the core domain (task management) consistent.

Development follows a spec-driven approach: all code is derived strictly from specs in the `/specs` directory using Claude Code and Spec-Kit Plus.

---

## Phase Roadmap

| Phase | Description | Status |
|-------|-------------|--------|
| I | In-Memory Python Console App | Complete |
| II | Web App | Planned |
| III | Chatbot Integration | Planned |
| IV | Persistent + API Layer | Planned |
| V | Cloud-Native AI Distributed System | Planned |

---

## Phase I — In-Memory Python Console App

### Features

1. **Add Task** — create a task with a required title and optional description; auto-incremented ID assigned
2. **View Tasks** — list all tasks with ID, title, description, and completion status
3. **Update Task** — modify a task's title and/or description by ID
4. **Delete Task** — remove a task by ID
5. **Mark Complete / Incomplete** — toggle a task's completion status by ID

### Tech Stack

| Concern | Choice |
|---------|--------|
| Language | Python 3.13+ |
| Package manager | uv |
| Build backend | hatchling |
| Storage | In-memory (no database) |
| External dependencies | None (stdlib only) |
| Dev tooling | Claude Code + Spec-Kit Plus |

### Data Model

| Field | Type | Notes |
|-------|------|-------|
| `id` | `int` | Auto-incremented, unique, never reused |
| `title` | `str` | Required |
| `description` | `str` | Optional, defaults to `""` |
| `completed` | `bool` | Defaults to `False` |

### Architecture

Clean 4-module separation inside `phase1/src/todo/`:

| Module | Responsibility |
|--------|---------------|
| `models.py` | `Task` dataclass — pure data, no logic |
| `store.py` | `TaskStore` — all business logic and in-memory storage |
| `console.py` | `ConsoleUI` — all `input()`/`print()` calls and menu rendering |
| `main.py` | Entry point — wires `TaskStore` into `ConsoleUI` |

---

## Prerequisites

- **Python 3.13+**
- **uv** — [install guide](https://docs.astral.sh/uv/getting-started/installation/)

---

## Setup & Run

```bash
# Clone the repository
git clone https://github.com/mohsinmirzamaad/evolution-of-todo.git
cd evolution-of-todo

# Navigate to Phase I
cd phase1

# Run — uv creates the virtual environment and installs automatically
uv run todo
```

---

## Usage

```
============================================================
  Todo App — Phase I
============================================================

============================================================
  1. Add Task
  2. View Tasks
  3. Update Task
  4. Delete Task
  5. Mark Complete / Incomplete
  6. Quit
============================================================
Choose an option (1-6):
```

**Example session:**

```
Choose an option (1-6): 1
Enter title: Buy groceries
Enter description (optional, press Enter to skip): milk, eggs, bread
Task added: [1] Buy groceries | milk, eggs, bread | Incomplete

Choose an option (1-6): 2
--- Your Tasks ---
[1] Buy groceries | milk, eggs, bread | Incomplete
------------------

Choose an option (1-6): 5
Enter task ID to toggle: 1
Task updated: [1] Buy groceries | milk, eggs, bread | Complete
```

Press `Ctrl+C` at any menu prompt to exit gracefully.

---

## Folder Structure

```
evolution-of-todo/
├── .spec-kit/
│   └── config.yaml             # Spec-Kit phase configuration
├── specs/
│   ├── overview.md             # Project overview spec
│   └── features/
│       └── task-crud.md        # Task CRUD feature spec
├── phase1/
│   ├── pyproject.toml          # Phase I uv project (script entry point)
│   └── src/
│       └── todo/
│           ├── __init__.py
│           ├── models.py       # Task dataclass
│           ├── store.py        # In-memory storage + business logic
│           ├── console.py      # Console UI — menu, input/output
│           └── main.py         # Entry point
├── pyproject.toml              # Root monorepo config
├── CLAUDE.md                   # Claude Code project instructions
└── README.md
```

---

## Development Approach

- **Spec-driven**: every feature is defined in `/specs` first; no code is written without a corresponding spec
- **Claude Code + Spec-Kit Plus**: AI-assisted development with structured spec management
- **No manual code outside specs**: implementation strictly follows acceptance criteria from the spec files
- **Clean code**: single-responsibility modules, explicit error handling, type annotations throughout
