# Task Scheduler — Design Patterns & Clean Code Demo

Educational project demonstrating design patterns and clean code principles.

## Description

Task Scheduler — task scheduling system with different ordering strategies:
- By creation time (FIFO)
- By priority
- By nearest deadline

## Implemented Patterns

1. **Factory** — `TaskFactory.create()` for creating tasks with uuid and timestamp
2. **Strategy** — 3 scheduling algorithms (FIFO, Priority, EarliestDue)
3. **Repository** — data storage abstraction (easy to replace with DB)
4. **Dependency Injection** — dependency assembly in `compose_default()`

## Clean Code Principles

- ✅ Immutable objects (`@dataclass(frozen=True)`)
- ✅ Single responsibility per class (SRP)
- ✅ Interfaces over concrete implementations (DIP)
- ✅ Readable names (`schedule()`, `due_datetime()`)
- ✅ Type hints and docstrings
- ✅ Short functions and methods

## Project Structure

```
asik7spd/
├── main.py              # All source code (~190 lines)
├── diagram.png          # UML class diagram
└── README.md            # This file
```

## How to Run

```powershell
cd C:\Users\user\Documents\asik7spd
python main.py
```

**Output:**
```
Order (by priority):
- High priority task (priority=10)
- Medium priority task (priority=5)
- Low priority task (priority=0)
```

## Requirements

Only standard Python libraries (uuid, datetime, abc, dataclasses) — no external dependencies.

## UML Diagram

![UML Class Diagram](diagram.png)

The diagram shows all classes, interfaces, and relationships between system components with pattern explanations.

## For Presentation

1. **Code** — `main.py` with comments and patterns
2. **Diagram** — visual representation of architecture

---

**Author:** Educational Demo Project  
**Date:** November 1, 2025
