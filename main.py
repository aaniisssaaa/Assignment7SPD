"""Task Scheduler — демонстрация паттернов проектирования и Clean Code

Паттерны:
- Factory: TaskFactory.create()
- Strategy: SchedulingStrategy с реализациями (FIFO, Priority, EarliestDue)
- Repository: TaskRepository интерфейс + InMemoryTaskRepository
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
    
    Clean Code: неизменяемая структура, понятные поля, метод due_datetime()
    """
    id: str
    name: str
    priority: int
    created_at: datetime
    due_in_minutes: Optional[int] = None

    def due_datetime(self) -> Optional[datetime]:
        """Возвращает момент дедлайна, если он задан."""
        if self.due_in_minutes is None:
            return None
        return self.created_at + timedelta(minutes=self.due_in_minutes)


# ==================== FACTORY PATTERN ====================

class TaskFactory:
    """Factory для создания задач с удобными значениями по умолчанию.
    
    Паттерн Factory инкапсулирует правила создания объектов.
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
    """Интерфейс репозитория задач.
    
    Паттерн Repository изолирует логику доступа к данным.
    Clean Code: минимальный интерфейс (ISP - Interface Segregation Principle).
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
    """Простая in-memory реализация репозитория."""
    
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
    """Strategy interface: получает список задач и возвращает упорядоченный список.
    
    Паттерн Strategy позволяет менять алгоритм планирования без изменения клиента.
    """
    
    @abstractmethod
    def order(self, tasks: List[Task]) -> List[Task]:
        pass


class FifoStrategy(SchedulingStrategy):
    """Простейшая стратегия: по времени создания (FIFO)."""
    
    def order(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda t: t.created_at)


class PriorityStrategy(SchedulingStrategy):
    """Сортирует по убыванию приоритета, затем по времени создания."""
    
    def order(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda t: (-t.priority, t.created_at))


class EarliestDueStrategy(SchedulingStrategy):
    """Сортирует по ближайшему дедлайну; задачи без дедлайна идут в конец."""
    
    def order(self, tasks: List[Task]) -> List[Task]:
        def key(t: Task):
            due = t.due_datetime()
            return (due or t.created_at.replace(year=9999), t.created_at)
        
        return sorted(tasks, key=key)


class Scheduler:
    """Контекст, который использует стратегию для планирования задач.
    
    Clean Code: Single Responsibility — только делегирует работу стратегии.
    """
    
    def __init__(self, strategy: SchedulingStrategy) -> None:
        self._strategy = strategy
    
    def schedule(self, tasks: List[Task]) -> List[Task]:
        """Возвращает новый список задач в порядке выполнения."""
        return self._strategy.order(tasks)


# ==================== DEPENDENCY INJECTION ====================

def compose_default() -> tuple[TaskRepository, Scheduler]:
    """Собирает приложение: InMemory репозиторий и Scheduler с PriorityStrategy.
    
    Упрощённая dependency injection: зависимости создаются в одном месте.
    """
    repo = InMemoryTaskRepository()
    scheduler = Scheduler(PriorityStrategy())
    return repo, scheduler


# ==================== DEMO ====================

def demo() -> None:
    """Демонстрация работы системы планирования задач."""
    repo, scheduler = compose_default()
    
    # Создаём задачи с разными приоритетами
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
