# dev-team-skills

[English](README.md) | [한국어](README_ko.md)

> A cross-platform (Windows & macOS) collection of AI coding agent skills and rules, inspired by Andrej Karpathy's engineering philosophy and practical senior engineering principles.  
> It helps you run a task-sized engineering squad with six accountable owners across major AI environments like **Google Antigravity**, **Claude Code**, **OpenAI Codex** (officially verified), and **Cursor** (experimental support), using **deterministic harness engineering** and **empirical comparative benchmarks** to ship reliable software.

---

## 🌟 Why dev-team-skills? (Empirical Benchmark Proof)

Rather than subjective prompt claims, `dev-team-skills` proves its value through **reproducible numerical benchmarks** across 19 pressure regression scenarios and 5 multi-turn engineering workflows:

### 📊 Comparative Benchmark Metrics

| Metric | Vanilla Agent (Baseline) | Unbounded Multi-Agent | **dev-team-skills (Lean Squad)** | Improvement (vs Baseline) |
| :--- | :---: | :---: | :---: | :---: |
| **1. Policy Enforcement / Safety Rate** | 21.1% (4/19) | 52.6% (10/19) | **100.0% (19/19)** | **+78.9%p (Full Protection)** |
| **2. Average Token Consumption** | 16,900 | 42,500 | **25,780** | **-39.3% (Token Savings)** |
| **3. Decision Round-trip Turns** | 1.6 turns | 5.8 turns | **2.2 turns** | **-62.1% (Turn Reduction)** |
| **4. Defect & Vulnerability Catch Rate** | 42.9% (6/14) | 100.0% (14/14) | **100.0% (14/14)** | **+57.1%p (All Caught)** |

> 📖 Detailed evaluation methodology: [Comparative Benchmark Report](evals/comparative-benchmark.md)  
> 🔬 Reproduce metrics: `python evals/benchmark_metrics.py evals/runs/2026-11-07-comparative-benchmark.json`

### 🔍 Qualitative Advantages

| Feature | Typical Prompt / Rule Lists | **dev-team-skills** |
| :--- | :--- | :--- |
| **Team Coverage** | Only single-coder or simple pair programming | **Six accountable owners with task-specific product, engineering, quality, security and delivery capabilities** |
| **Quality Check** | Relies on LLM hallucination ("I finished it") | **Deterministic evaluation harness (`verify-harness`) and self-healing loop** |
| **Packaging & Ecosystem**| Manual copy-pasting of text files | **100% compliant with Antigravity, Claude Code, and Codex marketplaces (Cursor experimental)** |
| **Engineering Mindset** | Unnecessary boilerplate and too many libraries | **Karpathy principles & Ponytail (Standard Library First, YAGNI, minimum code)** |
| **Communication** | Long, robotic, and tiring AI explanations | **Kakao Pay style PR template, next-action-first (ADHD-friendly), natural tone** |
| **Cross-Platform** | Fails often on Windows due to Linux-only commands | **Equal support for Windows (PowerShell) and macOS/Linux (Bash) with CI tests** |

---

## 🏛️ Constitution & Principles

[`GEMINI.md`](./GEMINI.md) | [`CLAUDE.md`](./CLAUDE.md) | [`CODEX.md`](./CODEX.md) | [`AGENTS.md`](./AGENTS.md)

1. **Don't assume. Don't hide confusion.**
   - Never write code based on assumptions if requirements are unclear. Show trade-offs and confirm with the user.
2. **Minimum code & Standard library first. (Ponytail & YAGNI)**
   - "The best code is the code you never wrote." Always try the standard library and native OS tools before adding external packages.
3. **Touch only what you must. Clean up your mess.**
   - Do not edit files or reformat code outside your task scope. Clean up temporary scripts and test data before finishing.
4. **Define success criteria. Loop until verified.**
   - Define a clear Definition of Done before finishing. Run real build, test, and health check commands to prove your solution works.
5. **High-Impact Communication & ADHD Optimization**
   - Skip long greetings. Lead with the conclusion and immediate next action. Focus on one step at a time.
6. **Cross-Platform Compatibility (Windows & macOS)**
   - Provide tested commands and scripts for both Windows (PowerShell) and macOS/Linux (Bash).

---

## 📦 Skills Collection

| Skill Name | Description | Key Features |
| :--- | :--- | :--- |
| **`engineering-squad`** | Six-owner squad & task-sized execution | Clear collaboration across planning, harness, dev, QA, test design, security, deployment, and SRE |
| **`brainstorming`** | Product planning, problem definition & idea generation | SCAMPER, HMW, RICE scoring, Lean PRD template, linked with `research` subagent |
| **`harness-engineering`** | AI agent evaluation harness & marketplace packaging | Deterministic oracles, 3-platform packaging (`plugin.json`, `.claude-plugin`, `.codex-plugin`), self-healing loop |
| **`code-review`** | High-ROI design pattern reviews by role | 3 severity tiers (🔴Must Fix / 🟡Review Needed / 🟢Suggestion), tailored checklists |
| **`ponytail`** | Pragmatic senior minimalist mindset | Standard library first, zero bloat, remove unnecessary dependencies |
| **`humanizer`** | AI prose pattern remover (English) | Strips AI staging, forced triads, empty filler, and robotic formality based on Wikipedia's guide |
| **`humanizer-kr`** | Natural Korean technical writing | Removes stiff AI translations, fixes awkward passive voice, keeps technical meaning |
| **`i-have-adhd`** | Focus workflow to prevent cognitive overload | Leads with next action, finishes with one single task, cuts distraction |

---

## 👥 Engineering Squad: six accountable owners

Fifteen former role names (fourteen specialists plus Lead) map to six owners. The Tier 1/2 decision-owner count changes from eight to six; neither number measures active agents or token savings.

| Owner | Consolidated responsibilities |
| --- | --- |
| Tech Lead | Cross-domain decisions, FinOps, handoffs, final plain-language editing |
| Product Lead | Planning, marketing, evidence, dissent experiments |
| Engineering Lead | Frontend, backend, data and AI/harness capabilities |
| Quality Lead | Test criteria/design, QA execution and AC evidence |
| Delivery Lead | DevOps, SRE, deployment and recovery |
| Security Review Engineer | Independent security plus separate compliance applicability/actions |

A documentation edit defaults to Lead combining duties plus independent Security; a feature activates Engineering/Quality; product or operational changes add the relevant owner. Assign narrow specialists only for distinct outputs or expertise. Required checks remain even when roles are combined.

Read the [canonical workflow](skills/engineering-squad/SKILL_en.md), [capability and legacy-name mapping](skills/engineering-squad/references/roles_en.md), and [decision governance](skills/engineering-squad/references/decision-governance_en.md). Every PR still needs current-head/base independent security PASS before merge; unresolved applicable compliance violations remain blocking. Keep kickoff/stop rules and user appeals.

External references are candidates, not proof of use. The [adoption contract](skills/engineering-squad/references/tool-adoption_en.md) separates DISCOVERED / INSPECTED / AVAILABLE / APPLIED / VERIFIED and actual PASS/FAIL/NOT_RUN evidence. The [dated shortlist](skills/engineering-squad/references/external-skill-references_en.md) covers Superpowers, skill-creator, Playwright CLI and the Agent Skills specification. Read only what the task needs.

The [design and debate](docs/superpowers/specs/2026-11-06-lean-squad-design.md) explains alternatives, objections and validation limits. Document reduction is not a measured token-efficiency gain.

---

## 🛍️ Marketplace Packaging & Deterministic Harness

This repository supports the packaging standards of **Google Antigravity**, **Claude Code**, and **OpenAI Codex** as a single bundle:

| Platform | Manifest / Catalog File | Active Rule & Skill Paths |
| :--- | :--- | :--- |
| **Google Antigravity** | `plugin.json` (metadata & prompts) | `rules/AGENTS.md` & `skills/*/SKILL.md` |
| **Claude Code** | `.claude-plugin/marketplace.json` & `.claude-plugin/plugin.json` | `CLAUDE.md` & `skills/*/SKILL.md` |
| **OpenAI Codex** | `.codex-plugin/plugin.json` & `plugin.json` | `CODEX.md` / `AGENTS.md` & `skills/*/SKILL.md` |

### 🔍 Deterministic Harness Verification (Cross-Platform)

Both shell entry points call the same Python validator. It parses all four JSON manifests (nonblank string `name`/`description`, and an object array `plugins` for the marketplace), safely parses each skill's leading and closed YAML frontmatter, rejects duplicate keys, and checks SHA-256 byte synchronization across the five constitution files. If any English constitution file is present, all five English files must exist and match too. It also enforces coded skill invariants — SKL-001 skill file locations, SKL-002 frontmatter name matching the folder, SKL-003 relative links resolving — and verifies that `skills/catalog.json`, generated from the skill folders by `scripts/build-catalog.py`, matches its schema (CAT-001) and has not drifted from the folders (CAT-002). A dry-run materialize diff (MIR-001) also checks that the committed `.agents/skills` mirror equals what the setup script would produce from `skills/`, byte for byte, without writing anything.

Requires **Python 3.10+** and **PyYAML**. JSON and hashing use the standard library; YAML uses a safe parser rather than a handwritten YAML implementation. Install the pinned dependency with the same interpreter the launcher uses (`python3`, then `python`, then Windows `py -3`):

```bash
python -m pip install -r scripts/requirements-harness.txt
```

```bash
# Windows (PowerShell)
.\scripts\verify-harness.ps1

# macOS / Linux (Bash)
./scripts/verify-harness.sh
```

`--root <path>` optionally selects another package directory. Exit codes: `0` package PASS, `1` invalid package, `2` missing prerequisites or invalid arguments. UTF-8 BOM, LF/CRLF and paths with spaces are supported. CI runs the same isolated normal/error fixtures through Bash and PowerShell on Linux, Windows and macOS. On Windows, run Bash tests from Git Bash so the subprocess uses Git Bash rather than WSL's `bash.exe`; from PowerShell select `HARNESS_LAUNCHER=pwsh`:

```bash
python -m unittest discover -s tests -v
# Choose an entry point with HARNESS_LAUNCHER=bash|pwsh|python (default: bash).
# PowerShell example: $env:HARNESS_LAUNCHER = 'pwsh'
# Windows Git Bash: export HARNESS_BASH="$(cygpath -w "$BASH")"
```

This is a **local package-structure contract**, not complete vendor-schema validation or proof of installation compatibility. Agent behavior, product tests and independent security review are explicitly `NOT_RUN` by this command; existing approval gates still apply.

### Agent decision regressions

[Fourteen pressure scenarios and runner](evals/README.md) check test-status honesty, stale security approval, tiered decision ownership, stop conditions, summary evidence and scoped rechecks. CI runs checker self-tests and a labeled replay of recorded native-agent decisions; it does not run a fresh model or prove tool execution. Policy/scenario/scorer hashes and separate semantic reviews prevent old or incomplete records from receiving a decision PASS.

```bash
python evals/run_evals.py --replay evals/runs/2026-11-06-lean-squad.json
```

### Using Superpowers alongside dev-team-skills

Read the [phase ownership and artifact-reuse contract](skills/engineering-squad/references/superpowers-compatibility_en.md). In COMBINED mode, dev-team owns kickoff/gates/cost/final explanation and Superpowers owns verified design/planning/implementation procedures. Confirm package identity, share current approvals, supplement gaps and recheck changed scope. Optional unavailability uses explicit STANDALONE mode; mandatory missing prerequisites block the affected phase. No automatic installation or claim of measured savings.

---

## 💻 Installation & Usage Guide

### 1. Google Antigravity (Officially Verified)

#### Option A: One-Touch Setup Script (Recommended)
Automatically link skills to Antigravity's discovery path (`.agents/skills/`) or machine-global path (`~/.gemini/config/skills/`):
```powershell
# Windows (PowerShell): Setup for current workspace
.\scripts\setup-antigravity.ps1 -Target workspace

# Or install globally for all Antigravity projects
.\scripts\setup-antigravity.ps1 -Target global
```
```bash
# macOS / Linux (Bash): Setup for current workspace
bash scripts/setup-antigravity.sh workspace

# Or install globally
bash scripts/setup-antigravity.sh global
```
> 📖 Why skills aren't discovered out-of-the-box & how progressive disclosure works: [Antigravity Guide](docs/antigravity-guide.md)

#### Option B: Marketplace Catalog or UI
- Go to **Customizations** > **Marketplace** in Antigravity IDE.
- Search for `dev-team-skills` and click **[Install]**.
- Or use the one-click card in chat:
  ```markdown
  <plugin-card catalog-id="dev-team-skills"></plugin-card>
  ```

#### Option C: Global Plugins Directory
```bash
# Windows (PowerShell) & macOS/Linux (Bash)
git clone https://github.com/DongJinNam/dev-team-skills.git ~/.gemini/config/plugins/dev-team-skills
```

#### Option C: Workspace Plugin
- Clone into `.agents/plugins/dev-team-skills` in your project root, or declare it in `.agents/plugins.json` to share with your team via Git.

---

### 2. Claude Code

#### Option A: Add Marketplace Catalog (Recommended)
Add this repo as a remote marketplace catalog and install with one command:

```bash
# 1. Add repository as a Claude Code marketplace
/plugin marketplace add DongJinNam/dev-team-skills

# 2. Install dev-team-skills plugin
/plugin install dev-team-skills
```

> **Via CLI directly**:
> ```bash
> claude plugin marketplace add DongJinNam/dev-team-skills
> claude plugin install dev-team-skills
> ```

#### Option B: Validate Plugin Locally
```bash
claude plugin validate
```

#### Option C: Project Memory Integration
- Place `CLAUDE.md` in your project root to load the constitution, and call skills from `skills/`.

---

### 3. OpenAI Codex

#### Option A: Add to Codex CLI (Recommended)
```bash
# 1. Register marketplace catalog
codex plugin marketplace add DongJinNam/dev-team-skills --ref main

# 2. Install plugin
codex plugin install dev-team-skills
```

#### Option B: Interactive Plugin Manager
- In Codex CLI, type `/plugins` to open the interactive manager, search for `dev-team-skills`, and enable it.

#### Option C: Project Agent Instructions
- Place `CODEX.md` or `AGENTS.md` in your project root. The agent will automatically load the rules and links to task-relevant capabilities when starting a session.

---

### 4. Cursor [EXPERIMENTAL]

> ⚠️ **Caution**: Cursor support is currently **experimental**. Subagent coordination and full harness verification are under active development. Do not assume 100% feature parity.

#### Option A: One-Touch Setup Script
Automatically installs Cursor's MDC rule (`.cursor/rules/engineering-squad.mdc`) and legacy `.cursorrules`:
```powershell
# Windows (PowerShell)
.\scripts\setup-cursor.ps1
```
```bash
# macOS / Linux (Bash)
bash scripts/setup-cursor.sh
```
> 📖 Cursor limitations and usage guide: [Cursor Guide](docs/cursor-guide.md)

---

## 📝 Pull Request Template (Kakao Pay Style)

Included at [`.github/pull_request_template.md`](./.github/pull_request_template.md) (and [`.github/pull_request_template_en.md`](./.github/pull_request_template_en.md)), inspired by the Kakao Pay tech blog post ["Slow PR, Fast Dev"](https://tech.kakaopay.com/post/kakaopayins-slow-pr-fast-dev/):

- `# What problem does this PR solve?`
- `# Why do we need this?`
- `# How was it solved?`
- `# Limitations & Trade-offs`
- `# Impact on Existing Features`
- `# Edge Cases & Failure Scenarios`
- `# Alternatives Considered & Reason for Choice`
- `# Review Points (Risk Level by File/Area 🔴🟡🟢)`

---

### Tiered decision ownership & Creative Rookie

Organize the six owners and delegated capabilities as **Tier 1 Tech Lead → Tier 2 domain owners → Tier 3 specialists**. Domain owners decide local alternatives; Tech Lead resolves cross-domain conflict from evidence and dissent. Preserve Rookie ideas and user appeals; fifteen ballots/eight votes are advisory on request. Seniority cannot waive security, compliance, budget or authorization. See [decision governance](skills/engineering-squad/references/decision-governance_en.md).

## 📜 License
MIT License
