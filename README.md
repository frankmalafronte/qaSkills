# Design QA Agent

A Claude Code showcase demonstrating vision-powered design QA. Claude Code fetches a Figma frame and a live webpage screenshot, compares them with its built-in vision, and produces a structured QA report — all without a separate API key (runs on the Pro plan).

A visible Chrome window opens during the screenshot step so you can watch the agent work in real time.

## Prerequisites

- Python 3.10+
- A Figma account with a Personal Access Token

## Setup

1. Clone the repo:
   ```bash
   git clone <repo-url>
   cd qaSkills
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install the Playwright browser:
   ```bash
   playwright install chromium
   ```

4. Configure your Figma token:
   ```bash
   cp .env.example .env
   # Edit .env and paste your Figma Personal Access Token
   ```
   Get a token at: **figma.com → Settings → Security → Personal access tokens**

5. Open this folder in Claude Code:
   ```bash
   claude .
   ```

## Usage

Paste this prompt into Claude Code (substituting your real URLs):

```
Compare this Figma design to the live page and write a QA report:
- Design: https://www.figma.com/design/abc123/My-Project?node-id=1-2
- Page: https://mysite.com/landing
```

Claude Code will:
1. Run `fetch_figma.py` → saves `design.png`
2. Run `screenshot_page.py` → opens a visible Chrome window, navigates, saves `webpage.png`
3. Read both images with its built-in vision and compare them
4. Write `report.json` (structured discrepancies) and `report.md` (readable summary)

## Scripts

| Script | Purpose |
|---|---|
| `fetch_figma.py` | Fetches a Figma frame as a 2× PNG via the Figma REST API |
| `screenshot_page.py` | Screenshots a live URL via Playwright (headed Chrome, 1440×900) |

### Run scripts individually

```bash
python fetch_figma.py --url "https://www.figma.com/design/abc123/...?node-id=1-2" --out design.png
python screenshot_page.py --url "https://example.com" --out webpage.png
```
