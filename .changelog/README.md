# Changelog fragments

One file per pull request that changes user-visible behavior. The
merge workflow (`../.github/workflows/changelog.yml`) moves the
fragments into `CHANGELOG.md` `[Unreleased]` and deletes the files,
so two PRs never edit the same changelog lines.

## File name

`<PR-number>-<short-slug>.md` — for example `41-entry-skill.md`.

## Content

Exactly one `### <Section>` heading and bullet lines:

```markdown
### Added

- Entry skill `using-dev-team-skills` routes plain-language requests.
```

Sections (Keep-a-Changelog order): `Added`, `Changed`, `Deprecated`,
`Removed`, `Fixed`, `Security`. One section per fragment; a PR with
changes in two sections writes two fragments.

## Rules

- This `README.md` and files starting with `_` are not fragments.
- A fragment with no section, no bullets, or two sections fails CI.
- A PR without a fragment only gets a CI warning, not a failure.
  Docs-only and test-only PRs normally skip the fragment.
- Never edit `CHANGELOG.md` by hand for a new change; write a
  fragment. The release workflow promotes `[Unreleased]` to a version.
