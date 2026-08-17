"""
Unit Test Suite for To-Do Manager
Author: Anees Shaikh
"""

import unittest
import os
from todo_manager import TaskManager, TaskNotFoundError

class TestTaskManager(unittest.TestCase):
    """Test cases for Task Manager CRUD & persistence."""
    def setUp(self):
        self.test_file = "test_tasks.json"
        self.manager = TaskManager(storage_file=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_task(self):
        task = self.manager.add_task("Test Python Project", "Work", "High")
        self.assertEqual(task.title, "Test Python Project")
        self.assertEqual(task.category, "Work")
        self.assertEqual(task.priority, "High")
        self.assertFalse(task.completed)

    def test_complete_task(self):
        task = self.manager.add_task("Complete Assignment")
        completed_task = self.manager.complete_task(task.task_id)
        self.assertTrue(completed_task.completed)

    def test_task_not_found(self):
        with self.assertRaises(TaskNotFoundError):
            self.manager.complete_task(999)

if __name__ == "__main__":
    unittest.main()
