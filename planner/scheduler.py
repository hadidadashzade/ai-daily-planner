import json
from datetime import datetime
from typing import List, Dict, Optional

# Default path for tasks JSON storage
TASKS_FILE = "data/tasks.json"

class Task:
    def __init__(self, title: str, due_date: Optional[str] = None, priority: int = 3):
        """
        Represents a single task item.

        :param title: The title or description of the task.
        :param due_date: Due date in 'YYYY-MM-DD' format as string, optional.
        :param priority: Task priority level (1 = highest, 5 = lowest), default is 3.
        """
        self.title = title
        self.due_date = due_date  # Due date as string or None if not set
        self.priority = priority
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp of task creation

    def to_dict(self) -> Dict:
        """
        Convert the Task object into a dictionary for JSON serialization.

        :return: Dictionary representation of the task.
        """
        return {
            "title": self.title,
            "due_date": self.due_date,
            "priority": self.priority,
            "created_at": self.created_at
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Task':
        """
        Create a Task instance from a dictionary.

        :param data: Dictionary containing task data.
        :return: Task instance.
        """
        task = Task(
            title=data["title"],
            due_date=data.get("due_date"),
            priority=data.get("priority", 3)
        )
        # Use stored created_at if present, otherwise current time
        task.created_at = data.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return task

class Scheduler:
    def __init__(self, filename: str = TASKS_FILE):
        """
        Manages the list of tasks, handles loading and saving.

        :param filename: JSON file path to load/save tasks.
        """
        self.filename = filename
        self.tasks: List[Task] = []
        self.load_tasks()

    def load_tasks(self):
        """
        Load tasks from the JSON file.
        Initializes with empty list if file doesn't exist or is invalid.
        """
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.tasks = [Task.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    def save_tasks(self):
        """
        Save current tasks list to JSON file in a readable format.
        """
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=2)

    def add_task(self, task: Task):
        """
        Add a new Task object and save the updated list.

        :param task: Task instance to add.
        """
        self.tasks.append(task)
        self.save_tasks()

    def delete_task(self, index: int):
        """
        Delete a task by its index and save the updated list.

        :param index: 0-based index of the task to delete.
        """
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_tasks()

    def get_tasks_sorted(self) -> List[Task]:
        """
        Return tasks sorted by priority ascending (1 highest) and due date ascending.

        Tasks without due date are placed at the end.

        :return: Sorted list of Task objects.
        """
        def due_date_key(task: Task):
            try:
                return datetime.strptime(task.due_date, "%Y-%m-%d") if task.due_date else datetime.max
            except Exception:
                return datetime.max

        return sorted(
            self.tasks,
            key=lambda task: (task.priority, due_date_key(task))
        )

# ----------------------------
# Uncomment for simple tests
# if __name__ == "__main__":
#     scheduler = Scheduler()
#     scheduler.add_task(Task("Test task 1", "2025-07-30", 2))
#     scheduler.add_task(Task("Test task 2", priority=1))
#     for i, task in enumerate(scheduler.get_tasks_sorted()):
#         print(f"{i+1}. {task.title} - Due: {task.due_date} - Priority: {task.priority}")
