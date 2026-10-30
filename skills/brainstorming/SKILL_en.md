---
name: brainstorming
description: >-
  Use this skill for product planning, ideation, requirement refinement, problem discovery, and market/technical research using structured brainstorming frameworks and research subagents.
---

# Product Planning & Structured Brainstorming

This skill is the standard guide for **Product Planners (PMs)** and Engineering Leads when designing new features or products. It helps you discover real user problems, run structured brainstorming, and turn ideas into a testable Minimum Viable Product (MVP) and Lean PRD (Product Requirement Document).

---

## 1. Core Planning Principles

1. **Problem First, Not Solution First**
   - Start with: "What is the user's biggest pain point?", not "What cool tech or feature should we build?"
   - Anti-pattern: Adding shiny tools or complex features without a clear problem to solve.
2. **Diverge, Then Converge**
   - Do not shoot down ideas too early based on feasibility. First explore many possibilities (Diverge), then use clear frameworks and data to pick the best ones (Converge).
3. **Hypothesis-Driven & Testable**
   - Every product idea should be a testable hypothesis.
   - Format: *"If we build [feature], [target users] will achieve [expected outcome], measured by [metric]."*

---

## 2. Structured Brainstorming Frameworks

### Divergence (Idea Generation)
- **SCAMPER**:
  - **S**ubstitute: Can we replace a step or tool with something simpler?
  - **C**ombine: Can we merge two separate features into one?
  - **A**dapt: Can we borrow a proven pattern from another domain?
  - **M**odify / Magnify: What is the single most valuable feature we can highlight?
  - **P**ut to other use: Can existing tools or data help a different user group?
  - **E**liminate: Can we delete unnecessary screens, steps, or inputs? (Ponytail mindset)
  - **R**everse: What if we reversed the process or started backwards?
- **How Might We (HMW)**:
  - Turn obstacles into opportunities: *"How might we help [user] achieve [goal] without [friction]?"*

### Convergence (Prioritization): RICE & MoSCoW
Score ideas to decide what to build first:

$$\text{RICE Score} = \frac{\text{Reach} \times \text{Impact} \times \text{Confidence}}{\text{Effort}}$$

- **MoSCoW Rules**:
  - **Must Have**: Core features required for launch (without these, the product is useless).
  - **Should Have**: Important features, but workarounds exist.
  - **Could Have**: Nice-to-have features if time permits.
  - **Won't Have (this time)**: Explicitly out of scope for the current MVP (Non-Goals).

---

## 3. Research & Data-Driven Discovery

Do not guess. Ground your decisions in real market and technical research.

### Research Workflow & Antigravity Built-in Tools
1. **Delegate to Research Subagent**:
   - For broad competitor or tech research, launch the `research` subagent (`invoke_subagent`) to get a fact-based summary without cluttering your main chat context.
2. **Web Search & Benchmarking**:
   - Use `search_web` to look up UX patterns, pricing, API docs, and user complaints for similar tools.
3. **Interactive Requirement Interviews**:
   - When facing architectural trade-offs, ask the user using the `/grill-me` command or call `ask_question`.

---

## 4. Lean PRD Template

Deliver a crisp Lean PRD using this simple format so the engineering squad can start building immediately:

```markdown
# [PRD] Feature / Product Name

## 1. Problem & Context
- **Background**: The pain point or inefficiency users face today.
- **Target User**: Who are we building this for?

## 2. Hypothesis & Value Proposition
- **Hypothesis**: Building [feature] will solve [pain point].
- **Key Metrics (KPI)**: How we measure success (e.g., cut task time by 50%, increase conversion by 15%).

## 3. MVP Scope
### Must Have (Core Features)
- [ ] Feature 1: Description
- [ ] Feature 2: Description

### Non-Goals (Out of Scope for this version)
- [ ] Out of scope item 1 (Follows YAGNI)
- [ ] Out of scope item 2

## 4. User Journey & Acceptance Criteria
- **Scenario**: Step-by-step user path from start to goal.
- **Given-When-Then Acceptance Criteria**:
  - *Given* the user is logged in
  - *When* they click this button
  - *Then* the result appears immediately.

## 5. Risks & Trade-offs
- Technical uncertainties, security constraints, and external dependencies.
```

---

## 5. Hand-off to Engineering Squad

Once the PRD is complete:
1. **Lead & AI Agent Engineer Review**: Check feasibility, testability, and eval harness needs.
2. **Interface Contracts**: Define API endpoints and DB entities based on the PRD user flow.
3. **Run Stages 1–5**: Data, Backend, and Frontend engineers build and verify the feature.
