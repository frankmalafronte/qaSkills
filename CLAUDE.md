# qaSkills — AI QA Agents

A collection of Claude Code sub-agents for automated QA workflows.

## Available agents

| Agent | Trigger |
|---|---|
| `design-qa-local` | Compare a Figma design to a live page and produce a QA report (runs locally) |

## Project scripts

| Script | Purpose |
|---|---|
| `fetch_figma.py` | Fetches a Figma frame as a 2× PNG via the Figma REST API |
| `screenshot_page.py` | Screenshots a live URL via Playwright (headed Chrome, 1440×900) |

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
cp .env.example .env  # add FIGMA_ACCESS_TOKEN
```
