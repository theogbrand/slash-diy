Diy-loop
* Uses external evaluator agent to write tests independently (to work with planner agent)
* After generation of single task/phase, run evaluator’s test and if it fails, we inject context to edit files to pass the test (without hacking)
