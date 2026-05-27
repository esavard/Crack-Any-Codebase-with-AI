"""Render the product story as markdown and clean HTML.

HTML rule from docs/codebase-rules.md §11: vanilla HTML, no JS framework, no
build step. The page is one self contained file. Mermaid is not used here
(this chapter is all prose + tables + cards).
"""
import html as _html
import os
import sys

from markdown_it import MarkdownIt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

_MD = MarkdownIt(
    "commonmark", {"html": False, "linkify": True, "breaks": False}
).enable(["table"])


def md(text):
    """Inline markdown to HTML for a short string. Strips the wrapping <p>...</p>."""
    if text is None:
        return ""
    rendered = _MD.render(str(text).strip())
    rendered = rendered.strip()
    if rendered.startswith("<p>") and rendered.endswith("</p>") and rendered.count("<p>") == 1:
        return rendered[3:-4]
    return rendered


def md_block(text):
    """Full markdown to HTML for a multi-paragraph string."""
    return _MD.render(str(text or "").strip())


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{name}: product story</title>
<style>
  :root {{ --fg: #0d1117; --muted: #57606a; --bg: #fff; --soft: #f6f8fa;
          --accent: #0969da; --rule: #d0d7de; --good: #2da44e; --warn: #bf8700; }}
  body {{ font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
         color: var(--fg); background: var(--bg); margin: 0 auto; max-width: 880px; padding: 32px 24px; }}
  h1 {{ font-size: 2em; margin: 0 0 .15em; }}
  h2 {{ font-size: 1.3em; margin: 2em 0 .4em; padding-bottom: .25em; border-bottom: 1px solid var(--rule); }}
  h3 {{ font-size: 1.05em; margin: 1.4em 0 .3em; }}
  p, li, td, th {{ color: var(--fg); }}
  p {{ margin: .6em 0; }}
  .muted {{ color: var(--muted); }}
  .pitch {{ font-size: 1.25em; line-height: 1.5; padding: 14px 18px; background: var(--soft);
            border-left: 3px solid var(--accent); border-radius: 4px; margin: .5em 0 1.5em; }}
  .pain {{ font-size: 1.05em; padding: 14px 18px; background: var(--soft); border-radius: 4px;
           margin: .5em 0 1.5em; border-left: 3px solid var(--warn); }}
  table {{ border-collapse: collapse; width: 100%; margin: .5em 0; }}
  th, td {{ border: 1px solid var(--rule); padding: 8px 10px; text-align: left;
            vertical-align: top; font-size: .92em; }}
  th {{ background: var(--soft); font-weight: 600; }}
  td .verdict {{ display: block; font-weight: 600; color: var(--fg); margin-bottom: 2px; }}
  td .detail {{ display: block; color: var(--muted); font-size: .9em; line-height: 1.45; }}
  td.row-head {{ background: var(--soft); white-space: nowrap; }}
  .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 1em 0; }}
  @media (max-width: 640px) {{ .two-col {{ grid-template-columns: 1fr; }} }}
  .card {{ border: 1px solid var(--rule); border-radius: 6px; padding: 14px 16px; background: #fff; }}
  .card h3 {{ margin: 0 0 .4em; font-size: 1em; }}
  .card.sacrifices h3::before {{ content: "—  "; color: var(--warn); }}
  .card.gains h3::before {{ content: "+  "; color: var(--good); }}
  .card ul {{ margin: .3em 0 0; padding-left: 1.2em; }}
  .card li {{ margin: .35em 0; font-size: .94em; }}
  .callout {{ margin: 1em 0; padding: 14px 18px; background: #fff8e1; border-left: 3px solid var(--warn);
              border-radius: 4px; font-size: .95em; }}
  .callout strong {{ display: block; margin-bottom: .3em; }}
  .dim-defs {{ margin: 0 0 1em; padding-left: 1.2em; }}
  .dim-defs li {{ margin: .25em 0; font-size: .95em; }}
  /* Vertical card list for surprises / absences. Each item is one self-contained block. */
  .item-list {{ list-style: none; padding: 0; margin: .5em 0 1.5em; }}
  .item-list > li {{ padding: 12px 0 14px; border-top: 1px solid var(--rule); }}
  .item-list > li:first-child {{ border-top: none; padding-top: 6px; }}
  .item-list .headline {{ font-weight: 600; font-size: 1.02em; color: var(--fg); }}
  .item-list .where {{ color: var(--muted); font-size: .88em; margin-top: 3px; line-height: 1.4; }}
  .item-list .where code {{ background: none; color: var(--muted); padding: 0; }}
  .item-list .body {{ color: var(--muted); font-size: .92em; line-height: 1.5; margin-top: 5px; }}
  .item-list .body code {{ background: var(--soft); color: var(--fg); }}
  code {{ font: .88em/1.4 ui-monospace, "SF Mono", Consolas, monospace;
          background: var(--soft); padding: 1px 5px; border-radius: 3px; }}
</style>
</head>
<body>
  <h1>{name}</h1>
  <p class="muted">A product story reverse engineered from the codebase.</p>

  <h2>The pitch</h2>
  <p class="pitch">{variant}</p>

  <h2>The pain</h2>
  <p class="pain">{pain}</p>

  <h2>Where it sits</h2>
  <p class="muted">Four dimensions that actually split this product from its competitors.</p>

  <div class="two-col">
    <div class="card sacrifices">
      <h3>What it gives up</h3>
      <ul>
{sacrifices_html}
      </ul>
    </div>
    <div class="card gains">
      <h3>What it gets in return</h3>
      <ul>
{gains_html}
      </ul>
    </div>
  </div>

  <div class="callout">
    <strong>Why incumbents can't copy this</strong>
{why_html}
  </div>

  <h3>Side by side: dimensions and competitors</h3>
  <ul class="dim-defs">
{dim_defs_html}
  </ul>
  <table>
    <thead><tr><th>Product</th>{dim_headers}</tr></thead>
    <tbody>
{competitor_rows}
    </tbody>
  </table>

  <h2>Hiding in the code</h2>
  <p class="muted">Features the README doesn't advertise. Each one is a bet about where the product is going next.</p>
  <ul class="item-list">
{present_items}
  </ul>

  <h2>Missing on purpose</h2>
  <p class="muted">Features every competitor ships that this codebase deliberately doesn't. Strategy is choosing what not to do.</p>
  <ul class="item-list">
{absent_items}
  </ul>
</body>
</html>
"""


def _esc(s):
    return _html.escape(str(s).strip())


def render_html(name, shared):
    positioning = shared["positioning"]
    surprises = shared["surprises"]

    dims = positioning["dimensions"]
    dim_defs = "\n".join(
        f'    <li><strong>{_esc(d["name"])}</strong>: {md(d["definition"])}</li>'
        for d in dims
    )
    dim_headers = "".join(f'<th>{_esc(d["name"])}</th>' for d in dims)

    competitor_rows = []
    for c in positioning["competitors"]:
        cells = "".join(
            f'<td><span class="verdict">{md(cell["verdict"])}</span>'
            f'<span class="detail">{md(cell["detail"])}</span></td>'
            for cell in c.get("cells", [])
        )
        competitor_rows.append(
            f'      <tr><td class="row-head"><strong>{_esc(c["name"])}</strong></td>{cells}</tr>'
        )
    competitor_rows = "\n".join(competitor_rows)

    sacrifices_html = "\n".join(
        f'        <li>{md(s)}</li>' for s in positioning.get("sacrifices", [])
    )
    gains_html = "\n".join(
        f'        <li>{md(g)}</li>' for g in positioning.get("gains", [])
    )
    why_html = md_block(positioning.get("why_incumbents_cannot_copy", ""))

    present_items = "\n".join(
        f'    <li>'
        f'<div class="headline">{md(p["headline"])}</div>'
        f'<div class="where">{md(p["where"])}</div>'
        f'<div class="body">{md(p["bet"])}</div>'
        f'</li>'
        for p in surprises["present"]
    )
    absent_items = "\n".join(
        f'    <li>'
        f'<div class="headline">{md(a["headline"])}</div>'
        f'<div class="where">{md(a["evidence"])}</div>'
        f'<div class="body">{md(a["tradeoff"])}</div>'
        f'</li>'
        for a in surprises["absent"]
    )

    return HTML_TEMPLATE.format(
        name=_esc(name),
        variant=md(shared["variant"]),
        pain=md(shared["pain"]),
        dim_defs_html=dim_defs,
        dim_headers=dim_headers,
        competitor_rows=competitor_rows,
        sacrifices_html=sacrifices_html,
        gains_html=gains_html,
        why_html=why_html,
        present_items=present_items,
        absent_items=absent_items,
    )


def render_markdown(name, shared):
    positioning = shared["positioning"]
    surprises = shared["surprises"]

    parts = [f"# {name}\n"]
    parts.append("_A product story reverse engineered from the codebase._\n")

    parts.append("## The pitch\n")
    parts.append(f"> {shared['variant']}\n")

    parts.append("## The pain\n")
    parts.append(f"> {shared['pain']}\n")

    parts.append("## Where it sits\n")
    parts.append("### What it gives up\n")
    for s in positioning.get("sacrifices", []):
        parts.append(f"- {s}")
    parts.append("")
    parts.append("### What it gets in return\n")
    for g in positioning.get("gains", []):
        parts.append(f"- {g}")
    parts.append("")
    parts.append("### Why incumbents can't copy this\n")
    parts.append(positioning.get("why_incumbents_cannot_copy", "").strip() + "\n")

    parts.append("### Side by side\n")
    parts.append("**Dimensions**\n")
    for d in positioning["dimensions"]:
        parts.append(f"- **{d['name']}**: {d['definition']}")
    parts.append("")
    headers = ["Product"] + [d["name"] for d in positioning["dimensions"]]
    parts.append("| " + " | ".join(headers) + " |")
    parts.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for c in positioning["competitors"]:
        cells = [f"**{c['name']}**"]
        for cell in c.get("cells", []):
            verdict = str(cell.get("verdict", "")).replace("\n", " ")
            detail = str(cell.get("detail", "")).replace("\n", " ")
            cells.append(f"**{verdict}**. {detail}")
        parts.append("| " + " | ".join(cells) + " |")
    parts.append("")

    parts.append("## Hiding in the code\n")
    for p in surprises["present"]:
        parts.append(f"### {p['headline']}")
        parts.append(f"_{p['where']}_")
        parts.append("")
        parts.append(p["bet"])
        parts.append("")

    parts.append("## Missing on purpose\n")
    for a in surprises["absent"]:
        parts.append(f"### {a['headline']}")
        parts.append(f"_{a['evidence']}_")
        parts.append("")
        parts.append(a["tradeoff"])
        parts.append("")

    return "\n".join(parts)
