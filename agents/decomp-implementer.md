---
name: decomp-implementer
description: "Implement or replace a dependency in diy_<package>/ based on a decomposition evaluation. Use during dependency decomposition (phase 1) after evaluation."
tools: Read, Grep, Glob, Bash, Write, Edit
---

# Decomposition Implementer

a. Save the `### Decompose` context given from the orchestrator agent to a file:
```bash
cat > decomp_context.md << 'EVAL'
<PASTE EVALUATION OUTPUT FROM STEP 2>
EVAL
```

b. Generate the inner ralph prompt:
```bash
uv run inner_ralph.py generate-prompt \
    --context decomp_context.md \
    --top-package <PACKAGE> \
    --sub-package <LIBRARY> \
    --max-iterations 30
```

c. Follow the generated prompt from step (b) to run the inner ralph loop until all Level 0 tests pass or max iterations are reached.

The inner ralph loop will:
- Verify baseline tests pass with the real library
- Rewrite imports to point at the DIY replacement
- Iteratively build `diy_<LIBRARY>/` until all Level 0 tests pass
- Commit each improvement and revert regressions

d. After the subagent finishes, discover new external imports:
```bash
grep -rh "^from \|^import " diy_<PACKAGE>/ --include="*.py" | sort -u
```

## Output Format

Report back with:
- **What was done:** <summary of changes>
- **New imports:** <list of external libraries that diy_<PACKAGE>/ now imports as a result>
