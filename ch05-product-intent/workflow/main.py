"""CLI: python main.py path/to/repo [--out ../output/]"""
import argparse, os, sys
from flow import create_product_story_flow
from render import render_html, render_markdown


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo_path")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    assert os.path.isdir(args.repo_path), f"{args.repo_path} is not a directory"

    name = os.path.basename(os.path.abspath(args.repo_path).rstrip('/'))
    out_dir = args.out or os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(out_dir, exist_ok=True)

    shared = {"repo_path": args.repo_path}
    create_product_story_flow().run(shared)

    md_path = os.path.join(out_dir, f"{name}-story.md")
    html_path = os.path.join(out_dir, f"{name}-story.html")

    open(md_path, "w").write(render_markdown(name, shared))
    open(html_path, "w").write(render_html(name, shared))

    print(f"\nWrote {md_path}")
    print(f"Wrote {html_path}")
    print(f"  Open {html_path} in a browser")


if __name__ == "__main__":
    main()
