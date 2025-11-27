"""
Module for saving and loading tasks
"""
import json
import os
from typing import List, Optional
from task_manager.models import Task


class TaskStorage:
    """Class for working with task storage"""
    
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.next_id = 1
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
                    if self.tasks:
                        self.next_id = max(task.id for task in self.tasks) + 1
            except (json.JSONDecodeError, KeyError):
                self.tasks = []
                self.next_id = 1
    
    def save_tasks(self):
        """Save tasks to file"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([task.to_dict() for task in self.tasks], f, ensure_ascii=False, indent=2)
    
    def add_task(self, task: Task) -> Task:
        """Add new task"""
        task.id = self.next_id
        self.next_id += 1
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task: Task):
        """Update task"""
        self.save_tasks()
    
    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID"""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self.save_tasks()
                return True
        return False
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return self.tasks
    
    def get_incomplete_tasks(self) -> List[Task]:
        """Get incomplete tasks"""
        return [task for task in self.tasks if not task.completed]
    
    def get_completed_tasks(self) -> List[Task]:
        """Get completed tasks"""
        return [task for task in self.tasks if task.completed]
