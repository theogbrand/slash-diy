---
name: decomp-implementer
description: "Implement or replace a dependency in diy_<package>/ based on a decomposition evaluation. Use during dependency decomposition (phase 1) after evaluation."
tools: Read, Grep, Glob, Bash, Write, Edit
---

# Decomposition Implementer

Read the file `.claude/inner-diy-loop.local.md` and follow its instructions.

## Output Format

- **COMPLETION PROMISE:** <promise>DONE</promise> or <promise>MAX ITERATIONS REACHED</promise>
- **What was done:** <summary of changes>
- **New imports:** <list of external libraries that diy_<PACKAGE>/ now imports as a result>
