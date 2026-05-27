"""Crawl a repo into a single string for an LLM.

Parameterized version. The defaults aim for "good baseline for most repos":
keep common source extensions, skip the noise the Ch3 chapter calls out (tests,
docs, examples, locales, vendored code, caches, build artifacts).

Override any default by passing your own set. The exposed constants are
frozensets so you can union or difference them:

    from utils import crawl, DEFAULT_SKIP_DIR
    # add to defaults:
    crawl("repo/", skip_dirs=DEFAULT_SKIP_DIR | {"my-generated-dir"})
    # restrict to one language:
    crawl("repo/", keep_ext={".py"})
"""
import os


# Source extensions across the common stacks.
DEFAULT_KEEP_EXT = frozenset({
    # web / scripting
    '.py', '.js', '.mjs', '.cjs', '.ts', '.tsx', '.jsx',
    '.vue', '.svelte', '.astro',
    '.rb', '.php', '.lua', '.pl',
    '.sh', '.bash', '.zsh', '.fish',
    # systems / compiled
    '.c', '.h', '.cpp', '.hpp', '.cc', '.cxx', '.hh',
    '.go', '.rs', '.zig', '.nim',
    '.java', '.kt', '.kts', '.scala', '.groovy',
    '.cs', '.fs', '.fsx',
    '.swift', '.m', '.mm',
    '.dart',
    # functional / niche
    '.ex', '.exs', '.erl', '.hs', '.clj', '.cljs',
    '.ml', '.mli', '.r', '.R', '.jl', '.cr',
    # smart contracts
    '.sol',
    # schema / IDL
    '.sql', '.proto', '.graphql', '.gql', '.thrift',
    # markup / docs / config (often the architecture)
    '.md', '.mdx', '.rst', '.adoc', '.txt',
    '.yaml', '.yml', '.json', '.toml', '.ini', '.cfg', '.conf',
    '.xml', '.html', '.htm',
    # styles
    '.css', '.scss', '.sass', '.less', '.styl',
    # templates
    '.ejs', '.hbs', '.handlebars', '.erb', '.jinja', '.j2', '.liquid',
})

# Extensionless filenames that ARE source. Without this set,
# os.path.splitext('Dockerfile')[1] == '' silently drops them.
DEFAULT_KEEP_NAMES = frozenset({
    'Dockerfile', 'Containerfile', '.dockerignore',
    'Makefile', 'GNUmakefile', 'Justfile',
    'Rakefile', 'Gemfile', 'Procfile', 'Vagrantfile', 'Brewfile',
    'CMakeLists.txt',
    'README', 'LICENSE', 'NOTICE',
    '.gitignore', '.gitattributes', '.editorconfig',
    '.env.example', '.env.sample',
})

# Directories to skip. Covers the noise categories the Ch3 chapter calls out:
# tests, docs, examples, locales, vendored code, build, caches.
DEFAULT_SKIP_DIR = frozenset({
    # vcs
    '.git', '.hg', '.svn',
    # python
    '__pycache__', 'venv', '.venv', 'env', '.tox', '.nox',
    '.pytest_cache', '.mypy_cache', '.ruff_cache', '.cache',
    # js / ts
    'node_modules', 'dist', 'build', '.next', '.nuxt', '.svelte-kit',
    '.turbo', '.parcel-cache', '.vercel', '.netlify', '.output',
    # go / rust / java / swift
    'target', 'vendor', '.gradle', 'Pods', 'DerivedData',
    # tests, docs, examples, i18n (the book §3.2 noise categories)
    'test', 'tests', '__tests__', 'spec',
    'docs', 'examples',
    'locales', 'translations', 'i18n',
    # generated assets
    'assets', 'generated', '__generated__', 'codegen',
    # coverage
    'coverage', 'htmlcov', '.nyc_output',
    # editors (debatable; usually noise)
    '.idea', '.vscode',
})

DEFAULT_MAX_FILE_BYTES = 500_000


def _wanted(filename, keep_ext, keep_names):
    if filename in keep_names:
        return True
    return os.path.splitext(filename)[1] in keep_ext


def list_files(root, *, keep_ext=DEFAULT_KEEP_EXT, skip_dirs=DEFAULT_SKIP_DIR,
               keep_names=DEFAULT_KEEP_NAMES, max_file_bytes=DEFAULT_MAX_FILE_BYTES):
    """Walk the tree and return paths that pass the filters. No file content read."""
    out = []
    skip = set(skip_dirs)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip]
        for f in sorted(filenames):
            if not _wanted(f, keep_ext, keep_names):
                continue
            path = os.path.join(dirpath, f)
            if max_file_bytes and os.path.getsize(path) > max_file_bytes:
                continue
            out.append(path)
    return out


def safe_read(path):
    """Read a file, skip per-file decode and permission errors.

    The only legitimate try/except in this module (and in the chapters that use
    it): one bad file should not kill a walk over 10,000 files.
    """
    try:
        return open(path, encoding='utf-8').read()
    except (UnicodeDecodeError, PermissionError):
        return None


def crawl(root, **kwargs):
    """Walk root, read every kept file, return one concatenated string with file headers."""
    files = list_files(root, **kwargs)
    parts = []
    for path in files:
        text = safe_read(path)
        if text is None:
            continue
        rel = os.path.relpath(path, root)
        parts.append(f"{'=' * 60}\nFile: {rel}\n{'=' * 60}\n{text}\n")
    return '\n'.join(parts)
