# Sprint 1 Design Document
## Extending Write Access in Home Assistant Driver

---

## 1. Background

Currently, the VOLTTRON Home Assistant driver supports:

- Read access for all Home Assistant entities.
- Write access only for `light` and `climate` domains.

The goal of this sprint is to design an architecture that enables write support for additional domains including:

- `switch`
- `cover`
- `fan`
- `lock`

No implementation is performed during this sprint.

---

## 2. Current Architecture Overview

### 2.1 Current Capability

- Read path is generic and supports all entities.
- Write path is domain-specific and implemented only for `light` and `climate`.

### 2.2 Current Write Flow

1. Driver receives a write request.
2. The entity domain is identified.
3. Domain-specific logic constructs the Home Assistant service call.
4. HTTP request is sent to the Home Assistant REST API.
5. Home Assistant routes the command to the device.

### 2.3 Identified Limitations

- Write logic is tightly coupled to specific domains.
- Adding support for new domains requires modifying driver logic.
- No abstraction layer exists for domain-specific write behavior.

---

## 3. API Analysis Across Domains

### 3.1 Domains Compared

- Existing: `light`, `climate`
- Target: `switch`, `cover`, `fan`, `lock`

### 3.2 Observed Patterns

- Some domains use binary semantics (`switch`, `lock`).
- Some require parameterized commands (`climate`, `cover`, `fan`).
- Some support optional extended parameters (`light`, `fan`).

### 3.3 Architectural Implication

Domain behavior varies significantly. A generalized conditional approach may not scale effectively as new domains are added.

---

## 4. Alternative Design Approaches

### 4.1 Option A — Extend Conditional Logic

Extend existing domain-based conditional branches in the driver.

Example conceptually:

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

**Pros**

- Minimal refactor required
- Low short-term development effort

**Cons**

- Conditional complexity grows linearly with domains
- Reduced maintainability
- Violates Open/Closed Principle

---

### 4.2 Option B — Domain Handler Abstraction (Strategy Pattern)

Introduce a domain-specific handler abstraction.

Each domain implements a handler responsible for constructing the service call.

Example interface:

```python
class WriteHandler:
    def supports(self, domain: str) -> bool:
        ...

    def build_service_call(self, command: str, value, entity_info: dict) -> dict:
        ...
```

Driver workflow:

```python
handler = handler_registry.get(domain)
service_call = handler.build_service_call(command, value, entity_info)
send_to_home_assistant(service_call)
```

**Pros**

- Clear separation of concerns
- Easier extensibility
- Improved maintainability
- Better alignment with software design principles
- Improved testability

**Cons**

- Requires moderate refactor
- Slightly higher initial complexity

---

## 5. Tradeoff Comparison

| Criteria | Option A | Option B |
|-----------|-----------|-----------|
| Implementation effort | Low | Medium |
| Scalability | Limited | Strong |
| Maintainability | Low | High |
| Extensibility | Difficult | Easy |
| Long-term sustainability | Weak | Strong |

---

## 6. Final Recommendation

Option B is recommended due to improved extensibility, maintainability, and architectural clarity for long-term support of additional Home Assistant domains.
