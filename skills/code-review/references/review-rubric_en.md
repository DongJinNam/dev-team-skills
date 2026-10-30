# Code Review Severity Rubric & Design Pattern Principles

This guide defines the severity rubric and design pattern principles used during code reviews.

---

## 1. 3-Tier Severity Criteria

### 🔴 [Must Fix] - Blocks Merging
Critical flaws that must be fixed before merging into the main codebase.
- **Security Flaws**: SQL injection, XSS, CSRF, broken auth/permissions, hardcoded secrets.
- **Data Integrity Issues**: Missing transactions causing partial updates, missing indexes causing full table scans, irreversible migrations.
- **System Crashes**: Infinite loops, deadlocks, unhandled Promise rejections, memory leaks (OOM).
- **Core Business Logic Bugs**: Wrong math in payments/pricing, invalid state machine transitions.

### 🟡 [Inquire & Verify] - Answer Required
Items that might not be hard bugs, but carry high risk or need architectural explanation.
- **Concurrency & Race Conditions**: Shared mutable state accessed without proper locks.
- **Trade-off Checks**: Understanding why the author chose higher memory over CPU speed (or vice versa).
- **Weak Error Handling**: Missing retries, timeouts, or fallbacks when calling 3rd-party APIs.
- **Tight Coupling**: Direct dependencies between domain modules that should be separate.

### 🟢 [Suggestion] - Optional (Does Not Block Merge)
Improvements for long-term health, readability, and maintenance.
- **Naming & Readability**: Better variable/function names that match standard domain terms.
- **DRY (Don't Repeat Yourself)**: Extracting helpers when logic is duplicated 3+ times.
- **YAGNI (You Aren't Gonna Need It)**: Removing unused parameters, dead code, or premature abstractions.
- **Modern Idioms**: Using standard library utilities and language built-ins.

---

## 2. Design Patterns & Architectural Principles

Reference these standard principles to give objective, constructive feedback:

### 1) SOLID Principles
- **SRP (Single Responsibility)**: "This function handles calculation, database writes, and email alerts all at once. Let's split these to keep each part focused."
- **OCP (Open-Closed)**: "Adding a new payment provider currently requires editing a huge if-else block. Using a simple Strategy pattern makes it easy to add new providers without touching existing code."
- **DIP (Dependency Inversion)**: "The service directly depends on a specific 3rd-party SDK. Introducing a small interface makes it easier to mock in unit tests."

### 2) Core Design Patterns (GoF)
- **Strategy Pattern**: Encapsulate different algorithms (e.g. discount rules, payment methods) so they can be swapped cleanly.
- **Factory Method**: Cleanly separate object creation when initializing instances involves complex conditional logic.
- **Adapter / Facade Pattern**: Wrap messy external APIs or legacy code behind a clean, simple interface.
