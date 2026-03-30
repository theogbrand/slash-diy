# Dependency Evaluation Policy

**Purpose:** Evaluate a single dependency in isolation to decide whether to keep it or replace it with a lower-level implementation.

**How to use:** When you need to decide if a dependency should be decomposed, consult this policy. Answer the questions in the evaluation framework or check if your dependency matches a "replace by default" category.

**Scope:** Language-agnostic. Focused on preventing unnecessary coupling and reducing surface area.

**Critical Context:** The decision to replace is not just about the library itself, but about how
it's used in your codebase. Even a "replace by default" library might be worth keeping if it's
deeply integrated. Even a well-written library might be cheap to replace if it's only used in
one place. Always assess both the library and its usage patterns before deciding.

---

## Usage Pattern Assessment

Before applying the evaluation framework below, assess how the dependency is used in your codebase:

**Breadth & Integration:**
- **Scope of usage:** How many files/modules depend on this? Is it isolated or pervasive?
- **Depth of integration:** Is it a thin wrapper (easy to replace) or a fundamental abstraction
  (baked into core logic)?
- **Coupling strength:** Are there strong assumptions about its behavior throughout the code?
  Tight coupling makes replacement costly and risky.

**Nature of Usage — Which Functions Matter:**
- **What specific functions/features are you using?** Not all functions in a library have equal
  replacement cost. A simple utility function is cheap to replace; a complex cryptographic
  algorithm is not.
- **Replaceability of used functions:** Can you replace the specific functions you use with
  simple alternatives, standard library equivalents, or inlined code? Or are they complex,
  unique functions that would be difficult to reimplement correctly?
- **Individual vs. bundle:** Are you using one simple function (can be extracted easily) or a
  suite of interdependent functions (harder to extract)?

**Decision guideline:**
- **Using simple, well-defined functions** → Easy to replace individually, even if library is
  complex overall.
- **Using complex, unique functions** → Hard to replace, even if only used in one place.
- **High breadth + deep integration + complex functions** → Decomposition is very expensive.
  Only replace if critical (security, maintenance, legal reasons).
- **Low breadth + isolated + simple functions** → Decomposition is cheap. Can replace even
  if library is otherwise acceptable.
- **Mixed** → Evaluate based on the framework below and risk tolerance.

---

## Replace by Default

The following categories should be replaced with lower-level implementations unless there is a specific reason to keep them:

*   **Vendor SDKs & API Wrappers** (e.g., `openai`, `slack-sdk`, `stripe-python`, `github3.py`, `boto3` for basic tasks).
    *   *Rationale:* High surface area. You typically only need 2-3 specific endpoints; a full SDK multiplies coupling and dependency risk.
    *   *Replacement strategy:* Write a lightweight, custom client using HTTP primitives (httpx, fetch, curl) and your project's data validation library (pydantic, zod). Map only the endpoints you actually call.

*   **AI/LLM "Glue" & Orchestration Frameworks** (e.g., `langchain`, `litellm`, `llama-index`).
    *   *Rationale:* Heavy transitive dependency trees. Core behavior is straightforward HTTP calls to a provider's API.
    *   *Replacement strategy:* Re-implement orchestration using standard control flow (if/while), string formatting, and direct HTTP calls to the provider's chat completion endpoint.

*   **Trivial Utilities** (e.g., `lodash`-equivalents, string/date manipulators).
    *   *Rationale:* Can be inlined with minimal code using language standard library.
    *   *Replacement strategy:* Write pure helper functions using standard library tools (itertools, datetime, collections, re in Python; lodash equivalents in JS; itertools in Rust).

*   **Deep/Unverifiable Dependency Trees.**
    *   *Rationale:* Packages with > 3 transitive dependencies create supply chain surface area and make auditing difficult.
    *   *Replacement strategy:* Extract and re-implement the core logic you need using a lower layer.

---

## Evaluation Framework for Unfamiliar Libraries

If a dependency does not match the above categories, apply this decision framework:

1.  **Does it implement a complex protocol?** (e.g., XML parsing, HTTP/2, Cryptography). If yes and it is well-governed → keep it.
2.  **Does it bridge to a lower-level language for performance/safety?** (e.g., bindings to C, Rust, or native code). If yes → likely worth keeping.
3.  **Is it solo-maintained without 2FA or recent commits?** If yes → replace it.
4.  **Can the core functionality be implemented in < 200 lines of code** using HTTP primitives or standard library? If yes → replace it.
