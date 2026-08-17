"""
Smart Task Manager & To-Do List Application
Author: Anees Shaikh
Description: Object-Oriented Python application with JSON file persistence, task filtering, and custom exception handling.
"""

import json
import os
from datetime import datetime

class TaskNotFoundError(Exception):
    """Custom exception raised when a requested task ID is not found."""
    pass

class Task:
    """Represents an individual To-Do Task."""
    def __init__(self, task_id: int, title: str, category: str = "General", priority: str = "Medium", completed: bool = False, created_at: str = None):
        self.task_id = task_id
        self.title = title
        self.category = category
        self.priority = priority.capitalize()
        self.completed = completed
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def mark_complete(self):
        """Mark task as completed."""
        self.completed = True

    def to_dict(self) -> dict:
        """Convert task object to dictionary for JSON serialization."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "category": self.category,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Reconstruct a Task object from a dictionary."""
        return cls(
            task_id=data["task_id"],
            title=data["title"],
            category=data.get("category", "General"),
            priority=data.get("priority", "Medium"),
            completed=data.get("completed", False),
            created_at=data.get("created_at")
        )

class TaskManager:
    """Manages collection of tasks with JSON persistence and filtering."""
    def __init__(self, storage_file: str = "tasks.json"):
        self.storage_file = storage_file
        self.tasks = []
        self.next_id = 1
        self.load_tasks()

    def add_task(self, title: str, category: str = "General", priority: str = "Medium") -> Task:
        """Add a new task with automatic ID assignment."""
        if not title.strip():
            raise ValueError("Task title cannot be empty.")
        
        task = Task(self.next_id, title.strip(), category.strip(), priority.strip())
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        return task

    def get_all_tasks(self, filter_completed: bool = None) -> list:
        """Retrieve all tasks, optionally filtered by status."""
        if filter_completed is None:
            return self.tasks
        return [t for t in self.tasks if t.completed == filter_completed]

    def complete_task(self, task_id: int) -> Task:
        """Mark a task as complete by ID."""
        task = self._find_task(task_id)
        task.mark_complete()
        self.save_tasks()
        return task

    def delete_task(self, task_id: int) -> Task:
        """Delete a task by ID."""
        task = self._find_task(task_id)
        self.tasks.remove(task)
        self.save_tasks()
        return task

    def _find_task(self, task_id: int) -> Task:
        """Helper to find task or raise TaskNotFoundError."""
        for t in self.tasks:
            if t.task_id == task_id:
                return t
        raise TaskNotFoundError(f"Task with ID {task_id} does not exist.")

    def save_tasks(self):
        """Save tasks list to JSON file."""
        try:
            data = {
                "next_id": self.next_id,
                "tasks": [t.to_dict() for t in self.tasks]
            }
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[Error] Failed to save tasks: {e}")

    def load_tasks(self):
        """Load tasks from JSON file if it exists."""
        if not os.path.exists(self.storage_file):
            return
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.next_id = data.get("next_id", 1)
                self.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        except Exception as e:
            print(f"[Warning] Could not load tasks from {self.storage_file}: {e}")

def main():
    """Interactive CLI menu for Task Manager."""
    manager = TaskManager()
    print("=" * 45)
    print("      SMART TASK MANAGER (PYTHON 3)")
    print("=" * 45)

    while True:
        print("\nOptions:")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Pending Tasks")
        print("4. Complete Task")
        print("5. Delete Task")
        print("6. Exit")

        choice = input("Enter choice (1-6): ").strip()
        try:
            if choice == "1":
                title = input("Enter task title: ")
                category = input("Enter category (Work/Personal/Study) [General]: ") or "General"
                priority = input("Enter priority (High/Medium/Low) [Medium]: ") or "Medium"
                task = manager.add_task(title, category, priority)
                print(f"✓ Task #{task.task_id} '{task.title}' added successfully!")

            elif choice == "2":
                tasks = manager.get_all_tasks()
                display_tasks(tasks)

            elif choice == "3":
                tasks = manager.get_all_tasks(filter_completed=False)
                display_tasks(tasks)

            elif choice == "4":
                task_id = int(input("Enter Task ID to complete: "))
                task = manager.complete_task(task_id)
                print(f"✓ Task #{task.task_id} marked as COMPLETED!")

            elif choice == "5":
                task_id = int(input("Enter Task ID to delete: "))
                task = manager.delete_task(task_id)
                print(f"✓ Task #{task.task_id} deleted.")

            elif choice == "6":
                print("Exiting Task Manager. Goodbye!")
                break
            else:
                print("[!] Invalid option. Please select 1 to 6.")
        except TaskNotFoundError as err:
            print(f"[!] Task Error: {err}")
        except ValueError as err:
            print(f"[!] Input Error: {err}")
        except Exception as err:
            print(f"[!] Unexpected Error: {err}")

def display_tasks(tasks):
    if not tasks:
        print("\nNo tasks found.")
        return
    print("\n" + "-" * 60)
    print(f"{'ID':<4} {'Status':<12} {'Priority':<10} {'Category':<12} {'Title'}")
    print("-" * 60)
    for t in tasks:
        status = "[DONE]" if t.completed else "[PENDING]"
        print(f"{t.task_id:<4} {status:<12} {t.priority:<10} {t.category:<12} {t.title}")
    print("-" * 60)

if __name__ == "__main__":
    main()
