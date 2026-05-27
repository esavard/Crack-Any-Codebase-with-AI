"""Crawl a repo into a single file you can paste into a chat window.

This is the 20-line script from §2.2 of the chapter. The chapter argues you should
do everything else by hand, so this script is the only code Chapter 2 ships.

Usage:
    python dump.py path/to/repo > dump.txt
"""
import os, sys

# Change these for your project.
EXTS = {'.py', '.md', '.txt', '.yaml', '.yml', '.json', '.toml',
        '.js', '.ts', '.tsx', '.jsx', '.go', '.rs', '.java', '.rb',
        '.sql', '.html', '.css'}
SKIP_DIRS = {'.git', 'node_modules', '__pycache__', 'venv', '.venv',
             'dist', 'build', 'test', 'tests', '.next', 'target', 'vendor'}


def crawl(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in sorted(filenames):
            if os.path.splitext(f)[1] in EXTS:
                rel = os.path.relpath(os.path.join(dirpath, f), root)
                try:
                    text = open(os.path.join(dirpath, f), encoding='utf-8').read()
                except (UnicodeDecodeError, PermissionError):
                    continue
                out.append(f"{'=' * 60}\nFile: {rel}\n{'=' * 60}\n{text}\n")
    return '\n'.join(out)


if __name__ == '__main__':
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    result = crawl(root)
    if len(sys.argv) > 2:
        open(sys.argv[2], 'w', encoding='utf-8').write(result)
        print(f"Wrote {len(result):,} chars to {sys.argv[2]}", file=sys.stderr)
    else:
        sys.stdout.write(result)
