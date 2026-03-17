from todo.models import Task


class TaskNotFoundError(Exception):
    def __init__(self, task_id: int) -> None:
        super().__init__(f"Task with ID {task_id} not found.")
        self.task_id = task_id


class TaskStore:
    def __init__(self) -> None:
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        if not title.strip():
            raise ValueError("Title is required and cannot be empty.")
        task = Task(id=self._next_id, title=title.strip(), description=description)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> list[Task]:
        return list(self._tasks)

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
    ) -> Task:
        task = self._find(task_id)
        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty.")
            task.title = title.strip()
        if description is not None:
            task.description = description
        return task

    def delete_task(self, task_id: int) -> Task:
        task = self._find(task_id)
        self._tasks.remove(task)
        return task

    def toggle_complete(self, task_id: int) -> Task:
        task = self._find(task_id)
        task.completed = not task.completed
        return task

    def _find(self, task_id: int) -> Task:
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(task_id)
