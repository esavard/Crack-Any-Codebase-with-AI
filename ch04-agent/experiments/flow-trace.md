I want to understand how this codebase actually works at the wire level, not as a feature list. Pick ONE specific user-visible action and trace it end to end.

## How to pick the action

Look at the README, entry points, public API, or CLI commands. Pick something that:

- A real user performs frequently. Not an edge case or a debug-only command.
- Is user-visible. "Clicking save", "running `gh pr create`", "submitting a chat message". NOT "RouterManager.dispatch".
- Crosses at least 5 files. Otherwise the trace teaches nothing.

If multiple candidates qualify, pick the one whose path most touches the codebase's named abstractions. That's the trace I'll learn the most from.

## What to do

Read the actual code, following imports and call sites. Don't guess. Don't reach for "typical patterns." If you take a wrong turn (read the interface file when the implementation is in a sibling folder, for example), call it out. The wrong turn is where I learn the layering rule.

## Output shape

```
## Action: [the action you picked]

[One sentence on why this action is representative.]

## Trace

1. **[Component]** (`path/to/file:line`) — what it does to the input.
2. **[Component]** (`path/to/file:line`) — what it does next.
   ...
   (5 to 15 hops. Don't shortcut. Show the boring middle.)

## Wrong turns I made

- [If any: what looked right, why it wasn't, what the convention turned out to be. If none, say so.]

## The gateway

[The single function where many entry points converge, if any. Example: "All file-open paths converge at editorService.openEditor(). Explorer click, Cmd+O, command palette: all land here." If there isn't one, say so explicitly.]

## For CLAUDE.md

[One sentence I should add to my skill file so future sessions skip this trace.]
```

## Calibration

Bad trace: "The user clicks save. The editor sends the buffer to the disk. The file system writes it. The UI updates."
Why bad: 4 hops, no file paths, no function names, no surprises. I learned nothing I couldn't have guessed.

Good trace: 12 hops through `EditorService.save()` → `TextFileService.save()` → `WorkingCopyFileService.save()` → `FileService.writeFile()` → `DiskFileSystemProvider.writeFile()` → back through `TextFileEditorModel.setDirty(false)` → `EditorGroupModel.unstick()` → status bar refresh. With the gotcha that `WorkingCopyFileService` runs three pre-save participants in order (backup, format, lint), and one of them (lint) can silently mutate the buffer before the disk write.
Why good: real path, real file names, surprises that only emerge from tracing across files.

## Rules

- Don't summarize the codebase first. Just trace.
- Use the real file paths and function names from the code you read.
- If a hop is "obvious", still include it. The boring middle is where the layering rules hide.
- If you can't find the gateway, that's a real finding. Say "no single gateway; each entry point has its own path" instead of inventing one.
