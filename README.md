# qaSkills — AI QA Agents

A collection of Claude Code agents for automated QA workflows.

---

## Agents

### design-qa-local

Vision-powered design QA. Fetches a Figma frame and a live webpage screenshot, compares them with Claude's built-in vision, and produces a structured HTML report. Runs locally — a visible Chrome window opens during the screenshot step.

**Trigger:** Give Claude Code a Figma URL and a live page URL and ask for a QA report.

```
Compare this Figma design to the live page and write a QA report:
- Design: https://www.figma.com/design/abc123/My-Project?node-id=1-2
- Page: https://mysite.com/landing
```

### web-test-cloud

Cloud agent. Inspects any URL's accessibility tree with Playwright, writes a Playwright/pytest test suite, runs it with a fix-and-retry loop, and commits passing tests to a new branch.

**Trigger (GitHub Actions):** Comment `/web-test` on an issue or PR, or trigger the `web-test-cloud` workflow manually with a URL.

> **Access:** Only repo collaborators with write access can trigger this agent directly. Everyone else should fork the repo and add their own `CLAUDE_ACCESS_TOKEN` secret.

---

## Setup

### Prerequisites

- Python 3.10+
- Node.js (for Claude Code CLI)
- A Figma Personal Access Token *(design-qa-local only)*

### Install

```bash
git clone <repo-url>
cd qaSkills

pip install -r requirements.txt
playwright install chromium
```

### Configure

```bash
cp .env.example .env
# Add your FIGMA_ACCESS_TOKEN (design-qa-local only)
```

Get a Figma token at: **figma.com → Settings → Security → Personal access tokens**

### For web-test-cloud (GitHub Actions)

Add a `CLAUDE_ACCESS_TOKEN` secret to your repo (Settings → Secrets → Actions). This is your Anthropic API key.

---

## Running design-qa-local

```bash
claude .
```

Then paste a prompt like:

```
Compare this Figma design to the live page and write a QA report:
- Design: https://www.figma.com/design/abc123/...?node-id=1-2
- Page: https://mysite.com/landing
```

## Running web-test-cloud

Comment on any issue or PR:

```
/web-test https://example.com
```

Or trigger manually via GitHub Actions → `web-test-cloud` → Run workflow.
