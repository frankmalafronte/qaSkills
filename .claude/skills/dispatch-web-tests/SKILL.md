---
name: dispatch-web-tests
description: Dispatch the web-test-cloud CI workflow to generate and run Playwright E2E tests for a URL
---

The user wants to generate Playwright E2E tests. Their instructions (may be empty):

> $ARGUMENTS

## What to do

1. Parse the instructions to extract the target URL (e.g. "google.com" → "https://google.com"). If no URL is found, ask the user for one before proceeding.

2. Dispatch the GitHub Actions workflow, passing the extracted URL and the full original instructions:

```bash
gh workflow run web-test-cloud.yml \
  -f url="<extracted-url>" \
  -f instructions="$ARGUMENTS"
```

3. Get the URL of the triggered run and report it to the user:

```bash
sleep 5 && gh run list --workflow=web-test-cloud.yml --limit=1 --json url -q '.[0].url'
```

Tell the user the run URL so they can monitor progress. Do not wait for the run to finish.
