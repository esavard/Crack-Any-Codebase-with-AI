Build this project from source and launch it. Don't ask me what commands to use. Figure it out.

## How to figure out the commands

Read in this order, stop as soon as you have enough:

1. The project's build config: `package.json`, `pyproject.toml`, `Cargo.toml`, `Makefile`, `Justfile`.
2. The canonical "getting started" script: `runs/speedrun.sh`, `scripts/dev.sh`, the top of the README.
3. The language version pin: `.nvmrc`, `.python-version`, `runtime.txt`, `rust-toolchain.toml`, `Dockerfile`.

## What to do

Run the install step. If it fails, READ THE ACTUAL ERROR MESSAGE. Apply ONE targeted fix and retry. Common targeted fixes:

- Wrong language version (the pin file said one thing, your env has another).
- Missing system dependency (a native module needs a system header).
- Missing build tool (cmake, pkg-config, a specific gcc version).

Don't reach for generic Stack Overflow patterns. Don't reach for `--force` or `--ignore-engines`. Don't downgrade dependencies. Read the error, fix the root cause, retry.

## Output shape

```
## Build timeline

| Step | Command | Duration | Result |
| ---- | ------- | -------- | ------ |
| Read config | (no command) | 10 sec | Found .nvmrc requiring Node 22.22.1 |
| Install (1st try) | `npm install` | 3 min | Failed: tree-sitter compilation error |
| Fix Node version | `nvm install 22.22.1` | 30 sec | Switched |
| Install (2nd try) | `npm install` | 1 min 36 sec | 1,710 packages installed |
| Compile | `npm run compile` | 1 min 9 sec | 0 errors |
| Launch | `./scripts/code.sh` | 12 sec | Running |
| **Total** | | **~5 min** | **Running build** |

## What I observed at runtime

[One or two things you could only learn by running the system, not reading the code. Examples:
- Number and topology of processes spawned.
- Activation order of extensions or plugins (often not what the README implies).
- Warnings the dev console fires that aren't documented.
- Default ports, default config files, default data directories.]

## For CLAUDE.md

```bash
# Build
[the exact commands that worked, in order]
```

Gotchas to remember:
- [Each version trap, native module fix, or undocumented step. One bullet each.]
```

## Calibration

Bad fix: "npm install failed, so I ran `npm install --force --legacy-peer-deps`."
Why bad: hides the root cause. The next person hits the same wall and either reapplies the same hack or gives up.

Good fix: "npm install failed with `gyp ERR! find Python implementations of distutils have been removed from Python 3.12+`. The repo's `.nvmrc` pins Node 22.22.1, but Node 22.22.1's gyp expects Python 3.11 distutils. Installed `setuptools` into the venv to restore distutils. Retried. Succeeded."
Why good: names the actual error, names the version mismatch, the fix is the root cause.

## Rules

- Three strikes and stop. If after three targeted fixes the build is still broken, surface the blocker. Don't loop.
- Don't fake the output. If a command actually ran for 4 minutes, write 4 minutes. If you didn't run it because the project doesn't build cold, say so.
- If the project is a library (no `main` to run), skip "Launch". Run the test suite instead. Same shape, different last row.
- Don't add ANY commands to CLAUDE.md that you didn't actually verify.
