# assets/ — provenance

Demo assets for P0-5 (top10-improvement-study-20261114.md §7). Every image is
rendered from a real output produced on 2026-11-14 in a worktree at main
40e0195. Nothing here is staged or synthesized. README.md does not reference
these files yet; P0-2 adds the hero references (`assets/demo.gif`,
`assets/social.png`), so merge P0-5 first, P0-2 after.

## Files

- `skill-trigger.png` (1120x702) — Codex native skill discovery
  (`python3 evals/check_skill_discovery.py --cwd .`), 13 skills found, 0 errors.
  `dev-team-skills:engineering-squad` is enabled, repo scope, with its real
  trigger description. This is the discovery listing, not a staged trigger
  event: no SessionStart hook exists yet (that is P1-1).
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

## Missing: `demo.gif`

No 15-second GIF is included, deliberately. This VM is headless: no display
or window system to capture, and no screen/terminal recorder installed (no
asciinema, terminalizer, or X server). An engineering-squad session is an
interactive agent conversation, not a CLI command, so there is no real
session to record here. A scripted terminal animation would be synthetic,
and this task forbids fake/synthetic GIFs. Revisit when a real recorded
session exists (e.g. a screen capture from a desktop run).

## Rendering

Rendered locally with Python PIL (DejaVu Sans Mono + Noto Sans CJK KR).
Reproduce with: `python3 /tmp/render-p05.py` (script is ephemeral; inputs are
the outputs listed above).
