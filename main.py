"""Task Scheduler — Design Patterns and Clean Code Demo

Design Patterns:
- Factory: TaskFactory.create()
- Strategy: SchedulingStrategy with implementations (FIFO, Priority, EarliestDue)
- Repository: TaskRepository interface + InMemoryTaskRepository
- Dependency Injection: compose_default()
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional
import uuid


# ==================== MODEL ====================

@dataclass(frozen=True)
class Task:
    """Immutable task model.
    
    Clean Code: immutable structure, clear fields, due_datetime() method
    """
    id: str
    name: str
    priority: int
    created_at: datetime
    due_in_minutes: Optional[int] = None

    def due_datetime(self) -> Optional[datetime]:
        """Returns the deadline datetime if set."""
        if self.due_in_minutes is None:
            return None
        return self.created_at + timedelta(minutes=self.due_in_minutes)


# ==================== FACTORY PATTERN ====================

class TaskFactory:
    """Factory for creating tasks with convenient default values.
    
    Factory pattern encapsulates object creation rules.
    """
    
    @staticmethod
    def create(name: str, priority: int = 0, due_in_minutes: Optional[int] = None) -> Task:
        return Task(
            id=str(uuid.uuid4()),
            name=name.strip(),
            priority=priority,
            created_at=datetime.utcnow(),
            due_in_minutes=due_in_minutes,
        )


# ==================== REPOSITORY PATTERN ====================

class TaskRepository(ABC):
    """Task repository interface.
    
    Repository pattern isolates data access logic.
    Clean Code: minimal interface (ISP - Interface Segregation Principle).
    """
    
    @abstractmethod
    def add(self, task: Task) -> None:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Task]:
        pass
    
    @abstractmethod
    def get_by_id(self, task_id: str) -> Optional[Task]:
        pass
    
    @abstractmethod
    def remove(self, task_id: str) -> None:
        pass


class InMemoryTaskRepository(TaskRepository):
    """Simple in-memory repository implementation."""
    
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}
    
    def add(self, task: Task) -> None:
        self._tasks[task.id] = task
    
    def get_all(self) -> List[Task]:
        return list(self._tasks.values())
    
    def get_by_id(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)
    
    def remove(self, task_id: str) -> None:
        self._tasks.pop(task_id, None)


# ==================== STRATEGY PATTERN ====================

class SchedulingStrategy(ABC):
    """Strategy interface: receives task list and returns ordered list.
    
    Strategy pattern allows changing scheduling algorithm without modifying client code.
    """
    
    @abstractmethod
    def order(self, tasks: List[Task]) -> List[Task]:
        pass


class FifoStrategy(SchedulingStrategy):
    """Simplest strategy: by creation time (FIFO)."""
    
    def order(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda t: t.created_at)


class PriorityStrategy(SchedulingStrategy):
    """Sorts by descending priority, then by creation time."""
    
    def order(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda t: (-t.priority, t.created_at))


class EarliestDueStrategy(SchedulingStrategy):
    """Sorts by nearest deadline; tasks without deadlines go to the end."""
    
    def order(self, tasks: List[Task]) -> List[Task]:
        def key(t: Task):
            due = t.due_datetime()
            return (due or t.created_at.replace(year=9999), t.created_at)
        
        return sorted(tasks, key=key)


class Scheduler:
    """Context that uses strategy for task scheduling.
    
    Clean Code: Single Responsibility — only delegates work to strategy.
    """
    
    def __init__(self, strategy: SchedulingStrategy) -> None:
        self._strategy = strategy
    
    def schedule(self, tasks: List[Task]) -> List[Task]:
        """Returns new list of tasks in execution order."""
        return self._strategy.order(tasks)


# ==================== DEPENDENCY INJECTION ====================

def compose_default() -> tuple[TaskRepository, Scheduler]:
    """Assembles application: InMemory repository and Scheduler with PriorityStrategy.
    
    Simplified dependency injection: dependencies created in one place.
    """
    repo = InMemoryTaskRepository()
    scheduler = Scheduler(PriorityStrategy())
    return repo, scheduler


# ==================== DEMO ====================

def demo() -> None:
    """Demonstration of task scheduling system."""
    repo, scheduler = compose_default()
    
    # Create tasks with different priorities
    repo.add(TaskFactory.create("Low priority task", priority=0))
    repo.add(TaskFactory.create("High priority task", priority=10))
    repo.add(TaskFactory.create("Medium priority task", priority=5))
    
    tasks = repo.get_all()
    ordered = scheduler.schedule(tasks)
    
    print("Order (by priority):")
    for t in ordered:
        print(f"- {t.name} (priority={t.priority})")


if __name__ == "__main__":
    demo()
