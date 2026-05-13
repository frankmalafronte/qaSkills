---
name: generate-tests
description: Trigger the Generate E2E Tests GitHub Actions workflow for the current branch's PR
---

Trigger E2E test generation by dispatching the GitHub Actions workflow for the current branch's PR.

## Steps

1. Get the current branch name:
   ```bash
   git branch --show-current
   ```

2. Find the open PR for this branch:
   ```bash
   gh pr view --json number,url,title
   ```
   If there is no open PR, tell the user they need to open one first and stop.

3. Dispatch the workflow, passing the PR number and any instructions the user provided:
   ```bash
   gh workflow run generate-e2e-tests.yml \
     --field pr_number=<number> \
     --field instructions="$ARGUMENTS"
   ```

4. Confirm to the user that the workflow was triggered and share the PR URL. Let them know Claude will commit the generated tests and post a summary comment on the PR when done.
