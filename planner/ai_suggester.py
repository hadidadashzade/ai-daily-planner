from datetime import datetime
from typing import List, Optional
from planner.scheduler import Task

class AISuggester:
    """
    A simple AI-powered task suggester class that provides recommendations
    based on task priority and due dates.

    This can be extended later with more complex AI or ML algorithms.
    """

    def suggest_next_task(self, tasks: List[Task]) -> Optional[Task]:
        """
        Suggest the next task to work on based on urgency and priority.

        Priority rules:
        1. Tasks due today or overdue have highest priority.
        2. Among those, tasks with the highest priority (lowest priority number) come first.
        3. If no urgent tasks, suggest the highest priority task regardless of due date.

        :param tasks: List of Task objects to choose from.
        :return: The suggested Task object, or None if no tasks available.
        """
        if not tasks:
            return None
        
        today = datetime.now().date()

        # Filter tasks that are due today or overdue
        urgent_tasks = [
            task for task in tasks 
            if task.due_date and datetime.strptime(task.due_date, "%Y-%m-%d").date() <= today
        ]

        if urgent_tasks:
            # Sort urgent tasks by priority (ascending) then by due date (earliest first)
            urgent_tasks.sort(key=lambda t: (t.priority, datetime.strptime(t.due_date, "%Y-%m-%d")))
            return urgent_tasks[0]

        # If no urgent tasks, return the highest priority task overall
        sorted_tasks = sorted(tasks, key=lambda t: t.priority)
        return sorted_tasks[0] if sorted_tasks else None

    def suggest_schedule(self, tasks: List[Task]) -> List[Task]:
        """
        Suggest an ordered schedule of tasks sorted by:
        1. Priority (ascending; 1 is highest)
        2. Due date (earliest first; tasks without due date come last)

        :param tasks: List of Task objects.
        :return: Sorted list of Task objects as suggested schedule.
        """
        return sorted(
            tasks,
            key=lambda t: (
                t.priority,
                datetime.strptime(t.due_date, "%Y-%m-%d") if t.due_date else datetime.max
            )
        )

# -----------------------------------------
# Testing block - uncomment to run standalone tests
# To run: python -m planner.ai_suggester

# if __name__ == "__main__":
#     from planner.scheduler import Scheduler
#
#     scheduler = Scheduler()
#     suggester = AISuggester()
#
#     all_tasks = scheduler.get_tasks_sorted()
#
#     next_task = suggester.suggest_next_task(all_tasks)
#     if next_task:
#         print(f"Next task to do: {next_task.title} (Priority: {next_task.priority}, Due: {next_task.due_date})")
#     else:
#         print("No tasks available.")
#
#     print("\nSuggested schedule:")
#     schedule = suggester.suggest_schedule(all_tasks)
#     for i, task in enumerate(schedule, 1):
#         print(f"{i}. {task.title} - Priority: {task.priority}, Due: {task.due_date}")
