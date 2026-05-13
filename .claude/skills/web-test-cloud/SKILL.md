---
name: generate-tests
description: Generate Playwright E2E tests based on free-form instructions or recent code changes
---

The user wants to generate Playwright E2E tests. Their instructions (may be empty):

> $ARGUMENTS

## What to do

Dispatch the GitHub Actions workflow to generate tests in the cloud:

```bash
gh workflow run generate-e2e-tests.yml \
  -f instructions="$ARGUMENTS"
```

Then get the URL of the triggered run and report it to the user:

```bash
sleep 3 && gh run list --workflow=generate-e2e-tests.yml --limit=1 --json url -q '.[0].url'
```

Tell the user the run URL so they can monitor progress. Do not wait for the run to finish.
