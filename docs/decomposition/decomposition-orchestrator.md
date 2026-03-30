# Decomposition Orchestrator

**Purpose:** Evaluate a single dependency from the queue and record the result.

**How to use:** After running `python scripts/decomp.py dequeue`, follow these steps.

---

## Overview

You have been handed a library name by the queue manager. Your job:

1. **Evaluate** it using the existing decomposition workflow
2. **Record** the decision (keep or decompose) via the queue manager
3. **Continue** to the next library

---

## Step 1: Evaluate

Run your chosen library through the single-pass evaluation:

- Read `dependency-decomposition-workflow.md` — this is the core evaluation logic
- Consult `decomposition-evaluation-policy.md` — does it match a "replace by default" category?
- Consult `library-decomposition-strategies.md` — if decomposing, what category is it?

Reach a decision: **keep** or **decompose**.

---

## Step 2: Record Decision

Based on your decision:

### If Keep

The library is valuable/necessary. Retain it as a direct dependency.

```bash
python scripts/decomp.py skip <library>
```

This removes the library from the queue. You're done with it.

### If Decompose

The library should be replaced with a lower-level implementation.

```bash
python scripts/decomp.py enqueue <library>
```

This:
1. Discovers the library's direct dependencies (using pip metadata)
2. Adds them to the queue as new candidates for evaluation
3. These become your next targets — you'll evaluate them one by one

The key principle: **always decompose one layer at a time.** If you decompose a high-level orchestration layer, you'll discover lower SDKs. Evaluate those next. Only later, if needed, decompose those further.

---

## Step 3: Continue

Get the next library from the queue:

```bash
python scripts/decomp.py dequeue
```

If the queue is empty, decomposition is complete. Otherwise, repeat the process.

---

## Important Rules

- **One library per cycle.** Evaluate exactly one, record the decision, move on.
- **Never skip levels.** If you decompose a wrapper library that uses lower SDKs, don't try to jump straight to the lowest layer. Evaluate the immediate dependencies first.
- **Use the referenced docs.** The workflow docs capture the decision framework. Don't invent new criteria.
- **Output the command.** When you're done with this library, show the command you're about to run so it's clear to any observer what happened.

---

## Example Session

```bash
$ python scripts/decomp.py dequeue
NEXT: urllib3

Queue: 2 remaining
...

# [You evaluate urllib3 using the workflow docs]
# Decision: KEEP (complex protocol, well-maintained, small surface area)

$ python scripts/decomp.py skip urllib3
Removed urllib3 from queue (kept)
Queue: 2 pending

$ python scripts/decomp.py dequeue
NEXT: certifi

Queue: 1 remaining
...

# [You evaluate certifi]
# Decision: DECOMPOSE (trivial cert bundle, can be inlined)

$ python scripts/decomp.py enqueue certifi
No new deps found for certifi
Queue: 1 pending

$ python scripts/decomp.py dequeue
NEXT: idna

Queue: 0 remaining
...

# [Continue until queue is empty]

$ python scripts/decomp.py dequeue
Queue empty. Decomposition complete.
```

---

## Referenced Documents

- `dependency-decomposition-workflow.md` — the single-pass evaluation framework
- `decomposition-evaluation-policy.md` — "replace by default" categories and evaluation criteria
- `library-decomposition-strategies.md` — taxonomy of library types and decomposition strategies
