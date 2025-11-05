"""Event Notification System - Observer Pattern Demo

Design Pattern: Observer (Behavioral)
- Subject: maintains list of observers, notifies them of state changes
- Observer: interface for objects that should be notified
- Concrete Observers: Logger, EmailNotifier, StatisticsCollector, AlertSystem

Clean Code Principles:
- Single Responsibility Principle (each observer has one job)
- Open/Closed Principle (easy to add new observers without modifying Subject)
- Interface Segregation (minimal observer interface)
- Dependency Inversion (depend on Observer abstraction)
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List
from enum import Enum


# ==================== EVENT MODEL ====================

class EventType(Enum):
    """Types of events in the system."""
    USER_REGISTERED = "user_registered"
    USER_LOGIN = "user_login"
    ORDER_PLACED = "order_placed"
    PAYMENT_RECEIVED = "payment_received"
    ERROR_OCCURRED = "error_occurred"


@dataclass(frozen=True)
class Event:
    """Immutable event model.
    
    Clean Code: immutable structure, clear fields, timestamp for tracking.
    """
    event_type: EventType
    user_id: str
    data: dict
    timestamp: datetime


# ==================== OBSERVER PATTERN ====================

class Observer(ABC):
    """Observer interface.
    
    Observer pattern: objects implementing this interface will be notified
    when events occur in the Subject.
    """
    
    @abstractmethod
    def update(self, event: Event) -> None:
        """Called when observed subject has new event."""
        pass


class Subject(ABC):
    """Subject interface (Observable).
    
    Maintains list of observers and notifies them of state changes.
    """
    
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """Attach an observer."""
        pass
    
    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """Detach an observer."""
        pass
    
    @abstractmethod
    def notify(self, event: Event) -> None:
        """Notify all observers about an event."""
        pass


# ==================== CONCRETE SUBJECT ====================

class EventManager(Subject):
    """Concrete Subject: manages events and notifies observers.
    
    Clean Code: Single Responsibility - only manages observers and notifications.
    """
    
    def __init__(self) -> None:
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"[EventManager] Attached: {observer.__class__.__name__}")
    
    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"[EventManager] Detached: {observer.__class__.__name__}")
    
    def notify(self, event: Event) -> None:
        """Notify all observers about event."""
        for observer in self._observers:
            observer.update(event)
    
    def trigger_event(self, event_type: EventType, user_id: str, data: dict) -> None:
        """Create and broadcast event."""
        event = Event(
            event_type=event_type,
            user_id=user_id,
            data=data,
            timestamp=datetime.utcnow()
        )
        print(f"\n[EventManager] Triggering: {event_type.value}")
        self.notify(event)


# ==================== CONCRETE OBSERVERS ====================

class LoggingObserver(Observer):
    """Logs all events to console.
    
    Observer pattern: reacts to events by logging them.
    """
    
    def update(self, event: Event) -> None:
        print(f"  [Logger] {event.timestamp.strftime('%H:%M:%S')} - "
              f"{event.event_type.value} by user {event.user_id}")


class EmailNotifier(Observer):
    """Sends email notifications for specific events.
    
    Observer pattern: selectively reacts to important events.
    """
    
    def __init__(self) -> None:
        self.important_events = {
            EventType.USER_REGISTERED,
            EventType.ORDER_PLACED,
            EventType.ERROR_OCCURRED
        }
    
    def update(self, event: Event) -> None:
        if event.event_type in self.important_events:
            print(f"  [Email] Sending notification for {event.event_type.value} "
                  f"to user {event.user_id}")


class StatisticsCollector(Observer):
    """Collects statistics about events.
    
    Observer pattern: maintains state based on observed events.
    """
    
    def __init__(self) -> None:
        self.event_counts: dict[EventType, int] = {}
    
    def update(self, event: Event) -> None:
        count = self.event_counts.get(event.event_type, 0)
        self.event_counts[event.event_type] = count + 1
        print(f"  [Stats] Event count for {event.event_type.value}: "
              f"{self.event_counts[event.event_type]}")
    
    def get_report(self) -> str:
        """Generate statistics report."""
        lines = ["\n=== Statistics Report ==="]
        for event_type, count in self.event_counts.items():
            lines.append(f"  {event_type.value}: {count} times")
        return "\n".join(lines)


class AlertSystem(Observer):
    """Monitors for critical events and raises alerts.
    
    Observer pattern: reacts to specific conditions.
    """
    
    def update(self, event: Event) -> None:
        if event.event_type == EventType.ERROR_OCCURRED:
            severity = event.data.get('severity', 'low')
            print(f"  [ALERT] Critical error detected! Severity: {severity}")
        elif event.event_type == EventType.PAYMENT_RECEIVED:
            amount = event.data.get('amount', 0)
            if amount > 1000:
                print(f"  [ALERT] Large payment received: ${amount}")


# ==================== DEMO ====================

def demo() -> None:
    """Demonstration of Observer pattern."""
    
    print("=== Observer Pattern Demo: Event Notification System ===\n")
    
    # Create Subject (Observable)
    event_manager = EventManager()
    
    # Create Observers
    logger = LoggingObserver()
    email_notifier = EmailNotifier()
    stats_collector = StatisticsCollector()
    alert_system = AlertSystem()
    
    # Attach observers to subject
    print("--- Attaching Observers ---")
    event_manager.attach(logger)
    event_manager.attach(email_notifier)
    event_manager.attach(stats_collector)
    event_manager.attach(alert_system)
    
    # Trigger various events
    print("\n--- Triggering Events ---")
    
    event_manager.trigger_event(
        EventType.USER_REGISTERED,
        user_id="user_001",
        data={"email": "alice@example.com"}
    )
    
    event_manager.trigger_event(
        EventType.USER_LOGIN,
        user_id="user_001",
        data={"ip": "192.168.1.1"}
    )
    
    event_manager.trigger_event(
        EventType.ORDER_PLACED,
        user_id="user_001",
        data={"order_id": "ORD123", "items": 3}
    )
    
    event_manager.trigger_event(
        EventType.PAYMENT_RECEIVED,
        user_id="user_001",
        data={"amount": 1500, "method": "credit_card"}
    )
    
    event_manager.trigger_event(
        EventType.ERROR_OCCURRED,
        user_id="system",
        data={"severity": "high", "message": "Database connection failed"}
    )
    
    # Demonstrate detaching an observer
    print("\n--- Detaching Email Notifier ---")
    event_manager.detach(email_notifier)
    
    event_manager.trigger_event(
        EventType.USER_LOGIN,
        user_id="user_002",
        data={"ip": "192.168.1.2"}
    )
    
    # Display statistics
    print(stats_collector.get_report())
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
