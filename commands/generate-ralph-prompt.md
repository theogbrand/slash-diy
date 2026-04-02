---
description: "Generate the runtime variables state body from a decomposition context"
argument-hint: "--context CONTEXT_FILE --top-package PACKAGE --sub-package LIBRARY [--max-iterations N]"
---

# Generate Ralph State Body

**Prerequisite:** `/test-curate` must have been completed first (curated test suite exists and passes against the real library). A decomposition context file (JSON or markdown evaluation output) must exist — see `examples/` for format.

Generate the runtime variables table for the inner diy loop state file:

```bash
uv run inner_ralph.py generate-state-body $ARGUMENTS
```

This outputs a markdown table of runtime variables (top_package, sub_package, category, strategy, etc.) that becomes the body of `.claude/inner-diy-loop.local.md`. The `--context` flag accepts JSON or markdown — format is auto-detected.

Print the generated state body to the user.
