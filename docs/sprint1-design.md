# Sprint 1 Design Document
## Extending Write Access in Home Assistant Driver

# Extending Write Access in the Home Assistant Driver

## Context and Scope

### Context

The current VOLTTRON Home Assistant (HA) Driver supports:

- Read access for all Home Assistant entities.
- Write access only for `light` and `climate` (thermostat) domains.

The Epic backlog item requires extending write-access functionality to currently unsupported device domains.

### Scope

In Scope:

- Architectural design to support write access for:
  - `switch`
  - `cover`
  - `fan`
  - `lock`
- Analysis of Home Assistant service APIs for these domains.
- Evaluation of alternative architectural approaches.
- Selection of a recommended design.

Out of Scope:

- Implementation of write functionality.
- UI changes.
- Performance optimization.
- Refactoring unrelated driver components.
- Supporting every possible Home Assistant domain.

---

## Goals and Non-Goals

### Goals

- Enable a scalable architecture for adding new write-supported domains.
- Maintain clean separation of concerns between driver logic and domain-specific logic.
- Minimize future modification effort when adding additional domains.
- Reuse existing HTTP communication mechanisms.

### Non-Goals

- Rewriting the entire driver architecture.
- Refactoring read functionality.
- Implementing plugin systems or dynamic loading.
- Optimizing runtime performance during this sprint.

---

## Proposed Design

We propose introducing a domain-specific handler abstraction using a Strategy Pattern approach.

### Architectural Overview

Instead of expanding conditional logic inside the driver, each supported domain will implement a `WriteHandler` abstraction responsible for constructing Home Assistant service calls.

Example interface:

```python
class WriteHandler:
    def supports(self, domain: str) -> bool:
        ...

    def build_service_call(self, command: str, value, entity_info: dict) -> dict:
        ...
```

Each domain implements its own handler:

```python
class LightHandler(WriteHandler):
    ...

class ClimateHandler(WriteHandler):
    ...

class SwitchHandler(WriteHandler):
    ...

class CoverHandler(WriteHandler):
    ...

class FanHandler(WriteHandler):
    ...

class LockHandler(WriteHandler):
    ...
```

Driver workflow:

```python
handler = handler_registry.get(domain)
service_call = handler.build_service_call(command, value, entity_info)
send_to_home_assistant(service_call)
```

### Key Properties

- The driver detects the entity domain.
- The appropriate handler is selected from a registry.
- The handler builds the domain-specific service call.
- A shared HTTP transport layer sends the request.

This ensures domain-specific logic is isolated from core driver logic.

---

## Alternatives Considered

### Option A — Extend Conditional Logic

Extend the existing implementation by adding domain-based conditional branches.

Example:

```python
if domain == "light":
    ...
elif domain == "climate":
    ...
elif domain == "switch":
    ...
elif domain == "cover":
    ...
```

Pros:

- Minimal refactor required.
- Lower short-term effort.

Cons:

- Conditional complexity grows with each domain.
- Reduced maintainability.
- Violates Open/Closed Principle.
- Harder to test domain logic independently.

---

### Option B — Domain Handler Abstraction (Chosen)

Introduce domain-specific handlers implementing a shared abstraction.

Pros:

- Clear separation of concerns.
- Easier extensibility.
- Better maintainability.
- Improved testability.
- Aligns with sustainable design principles.

Cons:

- Requires moderate refactoring.
- Slightly higher initial complexity.
- Requires handler registration mechanism.

---
---
| Criteria | Option A | Option B |
|-----------|-----------|-----------|
| Implementation effort | Low | Medium |
| Scalability | Limited | Strong |
| Maintainability | Low | High |
| Extensibility | Difficult | Easy |
| Long-term sustainability | Weak | Strong |

---
## Risks and Tradeoffs

### Risks

- Refactoring may introduce regression in existing write behavior.
- Inconsistent service API definitions across domains may complicate handler design.
- Over-abstraction could introduce unnecessary complexity if future domains are limited.

### Tradeoffs

- Increased architectural complexity vs long-term maintainability.
- Additional abstraction layer vs cleaner separation of concerns.
- Slight development overhead vs scalability for future growth.

---

## Open Questions

- Should handler registration be static or dynamically discovered?
- How should device capability differences be validated at runtime?
- Should validation logic reside inside handlers or in the driver?
- How should unsupported service responses from Home Assistant be handled?
- Should future domains reuse existing handler patterns or define specialized extensions?


## Final Recommendation

Option B is recommended due to improved extensibility, maintainability, and architectural clarity for long-term support of additional Home Assistant domains.
