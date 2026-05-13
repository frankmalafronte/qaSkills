---
name: web-test-cloud
description: Cloud agent. Inspects any URL's accessibility tree, writes a Playwright/pytest test suite, runs it in the cloud with a fix-and-retry loop, and commits passing tests to a new branch.
permissions:
  allow:
    - "Bash(.venv/bin/python .claude/agents/web-test-cloud/* *)"
    - "Bash(.venv/bin/pip install *)"
    - "Bash(.venv/bin/pytest *)"
    - "Bash(git checkout *)"
    - "Bash(git add *)"
    - "Bash(git commit *)"
    - "Bash(git push *)"
    - "Bash(gh workflow *)"
    - "Write(**)"
    - "Edit(**)"
---


## Workflow

### 1. Inspect the page

```bash
.venv/bin/python .claude/agents/web-test-cloud/inspect_page.py \
  --url "<url>" --out page_inventory.json
```

This captures the page's accessibility tree (YAML) and a full-page screenshot into `page_inventory.json`.

### 2. Write test_suite.py

Read `page_inventory.json`. Analyze the `accessibility_tree` field to understand the page structure, then write `test_suite.py` — a pytest file with these characteristics:

- Use `playwright.sync_api` with `sync_playwright`
- Prefer `page.get_by_role()`, `page.get_by_label()`, `page.get_by_text()` over CSS selectors
- One test function per meaningful interaction: page load, navigation links, search, CTAs, forms, etc.
- Each test is fully independent: launch browser, navigate to URL, assert, close
- Always use `headless=True` for all `sync_playwright` browser launches
- Use `pytest.mark.parametrize` only if multiple inputs share identical steps
- Import the URL from a constant at the top of the file: `BASE_URL = "<url>"`

### 3. Run tests

```bash
.venv/bin/pytest test_suite.py -v --tb=short
```

### 3b. On failure — fix and retry

If step 3 failed, read the pytest output to identify failing tests and their error traces. Fix only the test code (never the app). Re-run step 3. Repeat up to **3 attempts total**. If tests still fail after 3 attempts, stop and report all failures clearly.

### 4. Commit tests to a new branch

Create a branch with a descriptive name, commit `test_suite.py`, and push:

```bash
git checkout -b <branch>
git add -A
git commit -m "test: add E2E tests for <url>"
git push -u origin <branch>
```

If the instructions specify an existing branch to update, check it out instead of creating a new one.

Report the branch name and a summary of tests passed.

## Rules

- Never modify app code — only fix test code.
- If `inspect_page.py` fails, stop and report the error clearly.
- Always use `headless=True` for all Playwright browser launches — there is no display server in the cloud.
- Never write inline Python (`-c`, heredoc, etc.). Only call the scripts listed above and `pytest` directly.
- Be specific in test names: `test_nav_link_about` not `test_link`.
