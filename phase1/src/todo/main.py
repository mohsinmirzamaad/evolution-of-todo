from todo.store import TaskStore
from todo.console import ConsoleUI


def main() -> None:
    store = TaskStore()
    ui = ConsoleUI(store)
    ui.run()


if __name__ == "__main__":
    main()
