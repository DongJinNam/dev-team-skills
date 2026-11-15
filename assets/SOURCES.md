# assets/ — provenance

Demo assets for P0-5 (top10-improvement-study-20261114.md §7), plus the
15-second demo GIF recorded 2026-11-15 (Vooy #1). Every image is
rendered from a real output produced in a worktree. Nothing here is
staged or synthesized. README.md and README_ko.md reference
`assets/demo.gif` as the hero image right after the intro.

## Files

- `demo.gif` (1071x664, 7 frames, 11.6s playback) — real pty recording
  of three commands run 2026-11-15T09:30:56Z in a worktree at
  6df7d15: `bash scripts/verify-harness.sh` (31 PASS lines),
  `python3 evals/check_skill_discovery.py --cwd . --output /tmp/discovery.json`
  (`[{"skills": 14, "errors": []}]`),
  `python3 scripts/adapt.py --check` (`mirror matches skills/`).
  Pauses between commands are pacing so the output stays readable;
  no output is synthesized. Codex CLI could not run in this VM (no
  auth; `codex exec` loops on reconnect), so the GIF shows the package
  verification run instead of an agent session, and the alt text says
  so. Reproduce with `python3 /tmp/record_demo.py` (script is
  ephemeral).
- `skill-trigger.png` (1120x702) — Codex native skill discovery
  (`python3 evals/check_skill_discovery.py --cwd .`), 13 skills found, 0 errors.
  `dev-team-skills:engineering-squad` is enabled, repo scope, with its real
  trigger description. This is the discovery listing, not a staged trigger
  event. The SessionStart hook now exists (`hooks/hooks.json`); at the
  time this image was made it did not.
- `verify-harness.png` (1120x988) — verbatim output of
  `bash scripts/verify-harness.sh` (exit 0, 31 PASS lines). The NOT_RUN line
  is part of the real output.
- `ai-review.png` (1120x1003) — verbatim body of the real AI review comment
  on PR #35 (github-actions[bot], 2026-11-13T14:55:02Z, issuecomment-6856555627).
  Emoji are shown as `[!]` / plain numbers because this VM has no emoji font.
  Note: the original comment itself ends mid-word at `` `MAX_G `` — it was
  truncated at posting, not by this rendering.
- `social.png` (1200x630) — GitHub social preview graphic. Numbers are from
  README.md: vs Superpowers −15.61% tokens / −7.35% time (4-arm pilot, same
  model, 3 tasks each; small sample). To activate it, set it in the repo
  Settings (Social preview) in a browser — the API token has no
  Administration scope, so this cannot be done via API (403).

## Rendering

Rendered locally with Python PIL (DejaVu Sans Mono + Noto Sans CJK KR).
Reproduce PNGs with: `python3 /tmp/render-p05.py` (script is ephemeral;
inputs are the outputs listed above). Reproduce the GIF with:
`python3 /tmp/record_demo.py` (records the three commands in a pty and
renders the exact terminal bytes; script is ephemeral).
