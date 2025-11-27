"""
Data models for tasks
"""
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from typing import Optional


class Priority(Enum):
    """Task priority"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


@dataclass
class Task:
    """Class for representing a task"""
    id: int
    title: str
    description: str
    priority: Priority
    completed: bool = False
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def mark_completed(self):
        """Mark task as completed"""
        self.completed = True
        self.completed_at = datetime.now()
    
    def mark_incomplete(self):
        """Mark task as incomplete"""
        self.completed = False
        self.completed_at = None
    
    def to_dict(self):
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.name,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create task from dictionary"""
        return cls(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            priority=Priority[data['priority']],
            completed=data['completed'],
            created_at=datetime.fromisoformat(data['created_at']) if data['created_at'] else None,
            completed_at=datetime.fromisoformat(data['completed_at']) if data['completed_at'] else None
        )
