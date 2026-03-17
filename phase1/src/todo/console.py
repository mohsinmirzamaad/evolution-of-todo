from todo.models import Task
from todo.store import TaskNotFoundError, TaskStore

_DIVIDER = "=" * 60


class ConsoleUI:
    def __init__(self, store: TaskStore) -> None:
        self._store = store

    def run(self) -> None:
        print(_DIVIDER)
        print("  Todo App — Phase I")
        print(_DIVIDER)
        while True:
            try:
                self._show_menu()
                choice = input("Choose an option (1-6): ").strip()
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

            match choice:
                case "1":
                    self._handle_add()
                case "2":
                    self._handle_view()
                case "3":
                    self._handle_update()
                case "4":
                    self._handle_delete()
                case "5":
                    self._handle_toggle()
                case "6":
                    print("Goodbye!")
                    break
                case _:
                    print("Invalid option. Please enter a number between 1 and 6.")

    def _show_menu(self) -> None:
        print()
        print(_DIVIDER)
        print("  1. Add Task")
        print("  2. View Tasks")
        print("  3. Update Task")
        print("  4. Delete Task")
        print("  5. Mark Complete / Incomplete")
        print("  6. Quit")
        print(_DIVIDER)

    def _handle_add(self) -> None:
        title = input("Enter title: ").strip()
        if not title:
            print("Error: Title is required.")
            return
        description = input("Enter description (optional, press Enter to skip): ")
        try:
            task = self._store.add_task(title, description)
            print(f"Task added: {self._format_task(task)}")
        except ValueError as e:
            print(f"Error: {e}")

    def _handle_view(self) -> None:
        tasks = self._store.get_all_tasks()
        if not tasks:
            print("No tasks found. Add one first!")
            return
        print("--- Your Tasks ---")
        for task in tasks:
            print(self._format_task(task))
        print("------------------")

    def _handle_update(self) -> None:
        task_id = self._read_id("Enter task ID to update: ")
        if task_id is None:
            return
        try:
            tasks = self._store.get_all_tasks()
            current = next((t for t in tasks if t.id == task_id), None)
            if current is None:
                print(f"Error: Task with ID {task_id} not found.")
                return

            raw_title = input(
                f'Enter new title (press Enter to keep current: "{current.title}"): '
            )
            new_title = raw_title if raw_title.strip() else None

            raw_desc = input(
                f'Enter new description (press Enter to keep current: "{current.description}"): '
            )
            new_desc = raw_desc if raw_desc != "" else None

            task = self._store.update_task(task_id, title=new_title, description=new_desc)
            print(f"Task updated: {self._format_task(task)}")
        except TaskNotFoundError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")

    def _handle_delete(self) -> None:
        task_id = self._read_id("Enter task ID to delete: ")
        if task_id is None:
            return
        try:
            task = self._store.delete_task(task_id)
            print(f"Task deleted: {self._format_task(task)}")
        except TaskNotFoundError as e:
            print(f"Error: {e}")

    def _handle_toggle(self) -> None:
        task_id = self._read_id("Enter task ID to toggle: ")
        if task_id is None:
            return
        try:
            task = self._store.toggle_complete(task_id)
            print(f"Task updated: {self._format_task(task)}")
        except TaskNotFoundError as e:
            print(f"Error: {e}")

    def _format_task(self, task: Task) -> str:
        status = "Complete" if task.completed else "Incomplete"
        return f"[{task.id}] {task.title} | {task.description} | {status}"

    def _read_id(self, prompt: str) -> int | None:
        raw = input(prompt).strip()
        if not raw.isdigit():
            print("Error: Please enter a valid numeric ID.")
            return None
        return int(raw)
