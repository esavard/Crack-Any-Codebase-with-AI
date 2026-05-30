"""CLI: python main.py path/to/repo [--out ../output/]
                       [--include PATTERN ...] [--exclude PATTERN ...]

--include and --exclude use .gitignore-style patterns matched against each
file's path relative to the repo root. Both can be repeated.

Examples:
    # only feed core source dirs (helpful for repos that overflow context):
    python main.py /tmp/tigerbeetle \\
        --include 'src/vsr/**' --include 'src/lsm/**' \\
        --include 'src/tigerbeetle.zig' --include 'src/state_machine.zig'

    # drop common ballast that survives the default skip list:
    python main.py /tmp/nats \\
        --exclude 'server/test/**' --exclude '**/internal/testhelper/**'
"""
import argparse, os
from flow import create_product_story_flow
from render import render_html, render_markdown


def main():
    ap = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=__doc__)
    ap.add_argument("repo_path")
    ap.add_argument("--out", default=None)
    ap.add_argument("--include", action="append", default=[],
                    help=".gitignore-style pattern: keep only matching paths. Repeatable.")
    ap.add_argument("--exclude", action="append", default=[],
                    help=".gitignore-style pattern: drop matching paths. Repeatable.")
    args = ap.parse_args()

    assert os.path.isdir(args.repo_path), f"{args.repo_path} is not a directory"

    name = os.path.basename(os.path.abspath(args.repo_path).rstrip('/'))
    base_out = args.out or os.path.join(os.path.dirname(__file__), "..", "output")
    # One subfolder per project, matching ch03-workflow's output/<repo>-tour/ pattern.
    out_dir = os.path.join(base_out, f"{name}-story")
    os.makedirs(out_dir, exist_ok=True)

    shared = {
        "repo_path": args.repo_path,
        "include": args.include,
        "exclude": args.exclude,
        "pain_image_path_target": os.path.join(out_dir, "pain.png"),
    }
    create_product_story_flow().run(shared)

    md_path = os.path.join(out_dir, "index.md")
    html_path = os.path.join(out_dir, "index.html")

    open(md_path, "w").write(render_markdown(name, shared))
    open(html_path, "w").write(render_html(name, shared))

    print(f"\nWrote {md_path}")
    print(f"Wrote {html_path}")
    print(f"  Open {html_path} in a browser")


if __name__ == "__main__":
    main()
