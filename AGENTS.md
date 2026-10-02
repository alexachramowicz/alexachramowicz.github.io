# Repository instructions

## Project
This is a static personal portfolio with no build step or backend.
- `index.html`: page content, navigation, and links.
- `styles/main.css`: layout and appearance.
- `images/`: artwork, portraits, and logos.
- `notes.txt`: historical planning notes, not setup instructions.

## Conventions
Use plain HTML and CSS and preserve the existing four-space indentation.
Keep asset paths relative and match filename casing exactly.
Preserve image credits, unrelated content, and existing user changes.
Avoid adding frameworks, build tooling, or dependencies unless requested.
Keep HTML IDs unique and give images and links meaningful accessible names.
Make interactive content usable with a keyboard as well as a mouse.

## Local development
From the repository root, run `py -m http.server 8000` on Windows
(or `python3 -m http.server 8000` where Python uses that command).
Open http://localhost:8000. Stop the server with Ctrl+C.

## Validation
No automated tests or CI checks are currently configured.
Run `git diff --check` after changes.
For page changes, check desktop and narrow layouts, navigation, project links,
hover behavior, and keyboard access in a browser.
Verify changed local asset paths and internal anchor targets exist.
Report checks performed and any checks that were unavailable; do not describe
source inspection as browser testing.

## Git workflow
Inspect status and diff before editing; preserve existing user changes.
Keep changes focused and use `codex/<topic>` for new branches unless instructed otherwise.
Use a separate worktree when isolation is useful; worktrees do not copy uncommitted edits.
Review the final diff and stage only intended files.
Commit, push, or publish only when authorized.
