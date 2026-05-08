# qaSkills — AI QA Agents

A collection of Claude Code sub-agents for automated QA workflows.

## Available agents

| Agent | Trigger |
|---|---|
| `design-qa-local` | Compare a Figma design to a live page and produce a QA report (runs locally) |

## Project scripts

All agent scripts live alongside their agent definition in `.claude/agents/<agent-name>/`.

| Script | Purpose |
|---|---|
| `.claude/agents/design-qa-local/fetch_figma.py` | Fetches a Figma frame as a 2× PNG via the Figma REST API |
| `.claude/agents/design-qa-local/screenshot_page.py` | Screenshots a live URL via Playwright (headed Chrome, 1440×900) |
| `.claude/agents/design-qa-local/compare_images.py` | Creates a side-by-side comparison image |
| `.claude/agents/design-qa-local/diff_images.py` | Computes pixel-diff stats and saves an amplified diff image |
| `.claude/agents/design-qa-local/generate_report.py` | Generates the HTML QA report |

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
cp .env.example .env  # add FIGMA_ACCESS_TOKEN
```
