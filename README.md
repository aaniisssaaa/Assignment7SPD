# Event Notification System - Observer Pattern Demo

Educational project demonstrating design patterns and clean code principles.

## Description

Event Notification System - event-driven system where multiple observers react to events in real-time:
- Logging all events
- Sending email notifications for important events
- Collecting statistics
- Raising alerts for critical situations

## Implemented Pattern: Observer (Behavioral)

The Observer pattern defines a one-to-many dependency between objects. When the Subject (Observable) changes state, all registered Observers are automatically notified.

### Components:

1. **Subject (EventManager)** - maintains list of observers, notifies them of events
2. **Observer Interface** - defines `update()` method for all observers
3. **Concrete Observers**:
   - **LoggingObserver** - logs all events to console
   - **EmailNotifier** - sends notifications for important events
   - **StatisticsCollector** - tracks event counts
   - **AlertSystem** - monitors critical events and raises alerts

### Benefits:
- Loose coupling between Subject and Observers
- Easy to add new observers without modifying Subject
- Observers can be attached/detached dynamically at runtime

## Clean Code Principles

-  Immutable objects (`Event` with `frozen=True`)
-  Single Responsibility Principle (each observer has one job)
-  Open/Closed Principle (open for extension, closed for modification)
-  Interface Segregation (minimal Observer interface)
-  Dependency Inversion (depend on abstractions, not concrete classes)
-  Type hints and docstrings
-  Readable names (`attach()`, `notify()`, `update()`)

## Project Structure

```
asik7spd/
 main.py              # Complete implementation (~230 lines)
 diagram.png          # UML class diagram
 README.md            # This file
```

## How to Run

```powershell
cd C:\Users\user\Documents\asik7spd
python main.py
```

**Output:**
```
=== Observer Pattern Demo: Event Notification System ===

--- Attaching Observers ---
[EventManager] Attached: LoggingObserver
[EventManager] Attached: EmailNotifier
[EventManager] Attached: StatisticsCollector
[EventManager] Attached: AlertSystem

--- Triggering Events ---

[EventManager] Triggering: user_registered
  [Logger] 14:56:39 - user_registered by user user_001
  [Email] Sending notification for user_registered to user user_001
  [Stats] Event count for user_registered: 1

[EventManager] Triggering: payment_received
  [Logger] 14:56:39 - payment_received by user user_001
  [Stats] Event count for payment_received: 1
  [ALERT] Large payment received: $1500

--- Detaching Email Notifier ---
[EventManager] Detached: EmailNotifier

=== Statistics Report ===
  user_registered: 1 times
  user_login: 2 times
  order_placed: 1 times
  payment_received: 1 times
  error_occurred: 1 times
```

## Assignment Requirements

 **Design Pattern**: Observer pattern with Subject and multiple Observers  
 **Clean Code**: Immutability, SRP, OCP, ISP, DIP, type hints, docstrings  
 **UML Diagram**: Class diagram showing Observer pattern structure  
 **Real-World Application**: Event notification system (web apps, monitoring)  
 **Extensibility**: Easy to add new observers without modifying Subject

## Requirements

- Python 3.11+
- No external dependencies (standard library only)
