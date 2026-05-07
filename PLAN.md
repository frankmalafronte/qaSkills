# qaSkills — Project Plan

## Phase 1 — Single Page QA ✅
- [x] `fetch_figma.py` — fetch Figma frame as 2× PNG
- [x] `screenshot_page.py` — Playwright headed Chrome screenshot (1440×900)
- [x] `compare_images.py` — side-by-side composite with labels
- [x] `design-qa` agent — 5-step workflow: fetch → screenshot → composite → vision compare → report
- [x] `.venv` installed, `.venv/bin/python` hardcoded so no activation needed
- [x] Git repo pushed to github.com/frankmalafronte/qaSkills

## Phase 2 — Demo Video 🔄
- [ ] Get a Figma community file URL to use as test design
- [ ] Run end-to-end: design.png → webpage.png → comparison.png → report.md
- [ ] Record terminal + headed Chrome side by side (slow_mo=800 already set)
- [ ] Post to LinkedIn + update GitHub README

## Phase 3 — Multi-Page QA
Goal: give the agent a sitemap and have it QA every page automatically.

- [ ] `sitemap.json` — list of pages, each with a Figma frame URL and a live URL
- [ ] Agent loops through sitemap, runs the Phase 1 workflow per page
- [ ] Outputs one report per page + a rolled-up `summary_report.md`
- [ ] `screenshot_page.py` gains a `--click` or `--path` flag for navigating to specific states (e.g. open modal, go to /about)

## Phase 4 — Screen Map Navigation
Goal: agent can explore a live site on its own and build a map of what it finds.

- [ ] `map_site.py` — crawls internal links from a start URL, screenshots each page
- [ ] Agent matches crawled pages to Figma frames by name/slug
- [ ] Generates a `screen_map.json` pairing each live page to its design
- [ ] Feeds into Phase 3 multi-page QA automatically

## Phase 5 — Web App (future)
- FastAPI backend + frontend form
- Figma OAuth (no manual token)
- Deploy on Railway or Render
- Upload local images instead of Figma URL

## Phase 6 — Enhancements (future)
- Annotated diff image with bounding boxes highlighting issues
- Slack / email report delivery
- CI integration via GitHub Actions
