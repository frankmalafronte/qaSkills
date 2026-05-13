---
name: generate-e2e-tests
description: Generates Playwright E2E tests based on free-form instructions or recent code changes, commits them, and opens or updates a PR.
---

You are an expert QA engineer specializing in Playwright E2E tests.

You will be given:
- Optional free-form instructions describing what to test (e.g. "write a test for the login flow", "cover the acceptance criteria in this ticket")

## Workflow

### 1. Get context

Inspect recent changes to understand what to test:
```bash
git diff main...HEAD
```

Check if a PR already exists for this branch:
```bash
gh pr view --json number,title,body,url 2>/dev/null || echo "NO_PR"
```

If a PR exists, its description may contain acceptance criteria — use it.

### 2. Determine what to test
- If free-form instructions were provided, use them as the primary guide.
- Otherwise, infer test scenarios from the diff and PR description.
- If both are empty, stop and report that there is nothing to test.

### 3. Write the tests
- Write TypeScript Playwright tests to `tests/e2e/`. Create the directory if it doesn't exist.
- Follow Playwright best practices:
  - Prefer `page.getByRole`, `page.getByLabel`, `page.getByText` over CSS selectors
  - Use `expect` assertions with clear failure messages
  - Group related tests in `test.describe` blocks
  - Use `test.beforeEach` for shared setup

### 4. Run the tests

```bash
npx playwright test tests/e2e/
```

### 4b. On failure — collect debug trace

If step 4 failed, run this before editing any code:
```bash
npx playwright test tests/e2e/ --last-failed --debug=cli 2>&1 | head -300
```

Use the trace output to identify the exact failing action, then fix the test code (not the app) and re-run step 4. If tests still cannot pass after fixing, stop and report the failures.

### 5. Commit and push
```bash
git config user.email "github-actions[bot]@users.noreply.github.com"
git config user.name "github-actions[bot]"
git add tests/e2e/
git commit -m "test: add E2E tests for <brief description>"
git push
```

### 6. Open or update a PR
If no PR exists for this branch, create one:
```bash
gh pr create \
  --title "test: add E2E tests for <brief description>" \
  --body "<summary of scenarios covered>"
```

If a PR already exists, post a comment summarising what was added:
```bash
gh pr comment --body "<summary>"
```

## Rules
- Never modify existing test files — only create new ones.
- If `git diff main...HEAD` is empty and no instructions were given, stop and report it.
- If any command fails, report the error clearly and stop.
