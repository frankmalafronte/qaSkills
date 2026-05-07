import argparse
import base64
import json
from datetime import date
from pathlib import Path


SEVERITY_CONFIG = {
    "high":   {"color": "#c0392b", "bg": "#fdf0ef", "badge": "#e74c3c", "label": "🔴 High"},
    "medium": {"color": "#d35400", "bg": "#fef9ef", "badge": "#f39c12", "label": "🟡 Medium"},
    "low":    {"color": "#27ae60", "bg": "#f0faf4", "badge": "#2ecc71", "label": "🟢 Low"},
}


def encode_image(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode()


def build_issue_card(issue: dict) -> str:
    sev = issue["severity"].lower()
    cfg = SEVERITY_CONFIG.get(sev, SEVERITY_CONFIG["low"])
    return f"""
    <div class="card" style="border-left: 4px solid {cfg['badge']}; background: {cfg['bg']}">
      <div class="card-header">
        <span class="badge" style="background:{cfg['badge']}">{cfg['label']}</span>
        <span class="card-id">#{issue['id']}</span>
        <span class="card-category">{issue['category']}</span>
        <span class="card-location">{issue['location']}</span>
      </div>
      <div class="card-body">
        <div class="row"><span class="lbl">Design</span><span>{issue['design']}</span></div>
        <div class="row"><span class="lbl">Live</span><span>{issue['implementation']}</span></div>
        <div class="row"><span class="lbl">Fix</span><span>{issue['recommendation']}</span></div>
      </div>
    </div>"""


def generate_html(report: dict, comparison_b64: str, design_b64: str, live_b64: str,
                  figma_url: str, page_url: str) -> str:
    issues_by_sev = {"high": [], "medium": [], "low": []}
    for issue in report["discrepancies"]:
        sev = issue["severity"].lower()
        issues_by_sev.setdefault(sev, []).append(issue)

    sections = ""
    for sev in ["high", "medium", "low"]:
        items = issues_by_sev.get(sev, [])
        if not items:
            continue
        cfg = SEVERITY_CONFIG[sev]
        cards = "".join(build_issue_card(i) for i in items)
        sections += f"""
        <div class="section">
          <h2 style="color:{cfg['color']}">{cfg['label']} ({len(items)})</h2>
          {cards}
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Design QA Report</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
           background: #f5f6fa; color: #2d3436; padding: 32px; }}
    .header {{ background: white; border-radius: 10px; padding: 28px 32px;
               box-shadow: 0 2px 8px rgba(0,0,0,.08); margin-bottom: 24px; }}
    .header h1 {{ font-size: 22px; margin-bottom: 12px; }}
    .meta {{ display: flex; gap: 24px; font-size: 13px; color: #636e72; flex-wrap: wrap; }}
    .meta a {{ color: #0984e3; text-decoration: none; }}
    .totals {{ display: flex; gap: 12px; margin-top: 16px; flex-wrap: wrap; }}
    .total-chip {{ padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600; }}
    .summary {{ background: white; border-radius: 10px; padding: 20px 24px;
                box-shadow: 0 2px 8px rgba(0,0,0,.08); margin-bottom: 24px;
                font-size: 14px; line-height: 1.6; color: #555; }}
    .comparison {{ background: white; border-radius: 10px; padding: 20px 24px;
                   box-shadow: 0 2px 8px rgba(0,0,0,.08); margin-bottom: 24px; }}
    .comparison h2 {{ font-size: 16px; margin-bottom: 14px; }}
    .img-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 14px; }}
    .img-grid img {{ width: 100%; border-radius: 6px; border: 1px solid #dfe6e9; }}
    .img-label {{ font-size: 12px; color: #636e72; text-align: center; margin-top: 4px; }}
    .comparison-full img {{ width: 100%; border-radius: 6px; border: 1px solid #dfe6e9; }}
    .section {{ margin-bottom: 20px; }}
    .section h2 {{ font-size: 16px; margin-bottom: 12px; }}
    .card {{ background: white; border-radius: 8px; padding: 16px 18px;
             box-shadow: 0 1px 4px rgba(0,0,0,.06); margin-bottom: 10px; }}
    .card-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 10px;
                    flex-wrap: wrap; }}
    .badge {{ color: white; font-size: 11px; font-weight: 700; padding: 3px 8px;
              border-radius: 4px; }}
    .card-id {{ font-size: 12px; color: #b2bec3; }}
    .card-category {{ font-size: 13px; font-weight: 600; }}
    .card-location {{ font-size: 12px; color: #636e72; font-style: italic; }}
    .card-body {{ display: flex; flex-direction: column; gap: 6px; font-size: 13px; }}
    .row {{ display: flex; gap: 8px; line-height: 1.5; }}
    .lbl {{ min-width: 80px; font-weight: 600; color: #636e72; }}
  </style>
</head>
<body>
  <div class="header">
    <h1>Design QA Report</h1>
    <div class="meta">
      <span>📄 <a href="{page_url}" target="_blank">{page_url}</a></span>
      <span>🎨 <a href="{figma_url}" target="_blank">Figma design</a></span>
      <span>📅 {date.today().isoformat()}</span>
    </div>
    <div class="totals">
      <span class="total-chip" style="background:#fdf0ef;color:#c0392b">
        🔴 {len(issues_by_sev.get('high', []))} High
      </span>
      <span class="total-chip" style="background:#fef9ef;color:#d35400">
        🟡 {len(issues_by_sev.get('medium', []))} Medium
      </span>
      <span class="total-chip" style="background:#f0faf4;color:#27ae60">
        🟢 {len(issues_by_sev.get('low', []))} Low
      </span>
    </div>
  </div>

  <div class="summary">{report['summary']}</div>

  <div class="comparison">
    <h2>Screenshots</h2>
    <div class="img-grid">
      <div>
        <img src="data:image/png;base64,{design_b64}" alt="Figma Design">
        <div class="img-label">Figma Design</div>
      </div>
      <div>
        <img src="data:image/png;base64,{live_b64}" alt="Live Page">
        <div class="img-label">Live Page</div>
      </div>
    </div>
    <div class="comparison-full">
      <img src="data:image/png;base64,{comparison_b64}" alt="Side-by-side comparison">
      <div class="img-label">Side-by-side comparison</div>
    </div>
  </div>

  {sections}
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Generate HTML QA report from report.json and images")
    parser.add_argument("--report", default="report.json")
    parser.add_argument("--design", default="/tmp/design.png")
    parser.add_argument("--live", default="/tmp/webpage.png")
    parser.add_argument("--comparison", default="/tmp/comparison.png")
    parser.add_argument("--out", default="report.html")
    parser.add_argument("--figma-url", default="")
    parser.add_argument("--page-url", default="")
    args = parser.parse_args()

    report = json.loads(Path(args.report).read_text())
    comparison_b64 = encode_image(args.comparison)
    design_b64 = encode_image(args.design)
    live_b64 = encode_image(args.live)

    html = generate_html(report, comparison_b64, design_b64, live_b64, args.figma_url, args.page_url)
    Path(args.out).write_text(html)
    print(f"HTML report saved to {args.out}")


if __name__ == "__main__":
    main()
