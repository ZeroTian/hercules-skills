---
name: open-ended-research-orchestration
description: "Use when doing broad online technical research across papers, blogs, videos, repositories, docs, or competing approaches. Orchestrates Hermes source collection, Claude synthesis, Codex adversarial review, and durable research/task outputs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [research, web-research, synthesis, source-packet, claude, codex, orchestration]
    related_skills: [web-research, arxiv, youtube-content, claude-code, codex, hermes-collaborative-workflow, writing-plans]
---

# Open-Ended Research Orchestration

## Overview

Use this skill for exploratory technical research where the user wants information from many external sources — papers, blogs, videos, official docs, GitHub projects, demos, talks, and competing implementation approaches — and then wants that information turned into a project decision or implementation direction.

The core discipline is **source packet → synthesis → adversarial review → durable output**:

1. Hermes gathers and verifies sources.
2. Claude does the primary open-ended synthesis.
3. Codex reviews the synthesis adversarially.
4. Hermes records the validated conclusion, uncertainties, and next tasks.

Do not let any agent claim it researched the web without preserved URLs and source metadata.

## When to Use

Use when the user asks for:

- “调研一下方案 / 文章 / 论文 / 视频 / 博客 / repo”。
- Broad comparison of approaches before choosing an architecture.
- Research that should influence roadmap, specs, or implementation tasks.
- A technical landscape scan before coding.
- “Claude 和 Codex 谁适合做调研？” style workflow decisions.

Do not use for:

- A single factual lookup — fetch the source directly.
- Code review — use Codex / review skills.
- Implementation after the plan is already fixed — use coding workflow skills.
- Daily news digests — use `web-research` directly.

## Role Split

| Role | Responsibility | Default tools |
|---|---|---|
| Hermes | Scope the question, collect source packet, verify URLs, run agents, write final records | browser, terminal/curl, arxiv, youtube-content, web-research, repo reads |
| Claude / Claude Code | Research synthesis: compare approaches, map to project context, recommend MVP, draft plan | `claude -p` with read-only/source packet context |
| Codex | Adversarial review: source-to-claim check, overreach, conflicts with repo specs/code/tests, missing tests | `codex exec --sandbox danger-full-access` read-only review |

Rule of thumb:

- **Claude answers “what should we do and why?”**
- **Codex answers “is that conclusion actually supported and safe?”**
- **Hermes owns the evidence and final state.**

## Workflow

### 1. Narrow the Research Brief

Write a short brief before searching:

- Research question.
- Explicit exclusions / non-goals.
- Current project context to respect.
- Expected output: source packet, research note, implementation proposal, task entry, or all of these.
- Acceptance bar: how many credible sources, what types, and what must be verified.

Completion criterion: the brief is narrow enough that unrelated sources can be rejected.

### 2. Build a Source Packet

Collect sources with the most reliable available channel:

- Official docs/blogs: browser or curl/RSS.
- Papers: `arxiv` skill or arXiv web/API.
- Videos: `youtube-content` transcript workflow where available.
- GitHub repos: browser for trending/discovery, `gh` or git clone only when needed.
- Current project facts: read specs, roadmap, task ledger, and relevant code.

For each source record:

```text
title:
url:
type: paper | blog | docs | video | repo | issue | spec | code
date:
relevance: high | medium | low
key_takeaway:
confidence: high | medium | low
notes:
```

Completion criterion: every nontrivial claim in the later synthesis can point to at least one source row or an explicitly marked assumption.

### 3. Normalize and Filter Sources

Before synthesis:

- Remove duplicates.
- Prefer first-party or peer-reviewed sources over SEO summaries.
- Keep dissenting/negative sources when they change the decision.
- Mark unavailable or paywalled sources; do not invent their contents.
- Separate current project facts from external literature.

Completion criterion: the source packet is concise enough to fit in a Claude prompt without losing URLs and key takeaways.

### 4. Delegate Synthesis to Claude

Use Claude for open-ended reasoning over the source packet and repo context.

Prompt requirements:

- Include the research brief and source packet.
- Require source-grounded claims; cite source titles/URLs from the packet.
- Ask for: approach taxonomy, recommendation, rejected alternatives, risk list, MVP scope, non-goals, test strategy, and implementation-plan outline.
- Require explicit uncertainty labels when evidence is weak.
- Prohibit implementation or file writes unless the task is specifically to write a research note.

Typical command:

```bash
claude -p "$(cat /tmp/research_synthesis_prompt.md)" \
  --allowedTools 'Read' \
  --max-turns 8
```

Completion criterion: Claude returns a recommendation that is traceable to the packet and usable as a plan draft.

### 5. Delegate Adversarial Review to Codex

Use Codex after a proposal exists.

Prompt requirements:

- Provide the research brief, source packet, Claude synthesis, and relevant repo docs/specs.
- Ask Codex to verify whether each major conclusion is supported by sources.
- Ask for overreach/hallucination checks, missing counterexamples, repo-spec conflicts, and missing tests.
- Require PASS/FAIL with P0/P1/P2/P3 findings.
- Keep review read-only unless explicitly updating a research note or task ledger.

Typical command:

```bash
codex exec --sandbox danger-full-access "$(cat /tmp/research_review_prompt.md)"
```

Completion criterion: Codex either passes the proposal or lists concrete findings with source/line references.

### 6. Reconcile the Review

Do not treat Claude synthesis as the final research output when Codex returns findings.

- If Codex returns PASS: use the synthesis as the base, preserving any minor review notes.
- If Codex returns `not PASS as-is` with no P0/P1: keep the useful direction, but write a **revised recommendation** that incorporates every P2/P3 finding before creating tasks or docs.
- If Codex returns P0/P1: do not create implementation tasks; revise the source packet/brief or record blockers.
- Convert review findings into explicit acceptance criteria or tests when they affect implementation.
- Downgrade overstrong claims unless the source packet directly supports them.

When a research task reveals reusable nuance, add a concise case study under `references/` and point to it from the final report. Example: `references/personas-llm-judge-s3-case-study.md`.

Completion criterion: the final conclusion is the reviewed/reconciled conclusion, not the raw synthesis.

### 7. Hermes Finalizes

After reconciliation:

- If PASS or corrected-without-P0/P1: summarize the validated conclusion, write/patch `docs/research/` or task records when appropriate, and propose or create the next task.
- If blocked by P0/P1: do not implement; revise the source packet/synthesis or record blockers.
- Keep open questions separate from acceptance criteria.
- If the research affects a repo, update roadmap/spec/task files only after the conclusion is validated.

Completion criterion: the user can see what was decided, what evidence supports it, what changed after review, what remains uncertain, and what the next owner/action is.

## Output Templates

### Source Packet

```markdown
# <Topic> Source Packet

## Research brief

- Question:
- Non-goals:
- Project context:
- Expected output:

## Sources

| # | Title | Type | URL | Date | Relevance | Key takeaway | Confidence |
|---|---|---|---|---|---|---|---|
| 1 | ... | paper | ... | ... | high | ... | high |

## Initial observations

- Source-backed observation.
- Explicit assumption.
- Open question.
```

### Synthesis Brief for Claude

```markdown
You are the synthesis researcher. Use only the source packet and repo context below.

Deliver:
1. Approach taxonomy
2. Recommendation for this project
3. Alternatives rejected and why
4. MVP scope and non-goals
5. Risks and mitigations
6. Test/verification strategy
7. Implementation-plan outline
8. Uncertainties that need more evidence

Do not invent sources. Cite source row numbers or URLs for major claims.
```

### Codex Review Brief

```markdown
You are the adversarial research reviewer.

Review the source packet and Claude synthesis for:
- Unsupported or overextended claims
- Missing counterexamples
- Conflicts with repo specs/code/tests
- Unsafe scope expansion
- Missing tests or validation gates

Return PASS or findings grouped P0/P1/P2/P3. Cite source rows, URLs, and repo paths.
```

## Common Pitfalls

1. **Agent-invented bibliography.** Hermes must collect or verify sources; do not accept unsupported citations.
2. **Starting too broad.** Narrow the brief before searching, or synthesis becomes a generic literature review.
3. **Codex first for open-ended direction.** Codex is better after a proposal exists; use it to attack the conclusion.
4. **Implementing from unreviewed research.** Research that changes architecture should pass review before becoming tasks.
5. **Publishing raw synthesis after review findings.** If Codex returns `not PASS as-is`, reconcile the findings first; the durable doc should contain the revised recommendation, not the unedited synthesis.
6. **Conflating speculation with acceptance criteria.** Mark weak evidence as uncertainty, not as a requirement.
7. **Over-indexing on blogs.** Prefer first-party docs, papers, and working repos when decisions affect implementation.
8. **Dropping URLs in summaries.** Preserve source metadata so claims remain auditable.
9. **Ignoring local project facts.** External best practices do not override current specs, tests, and constraints without an explicit decision.
10. **Missing coverage semantics.** When research proposes a batch/panel/reporting workflow, require missing/failed item accounting and aggregation semantics before task creation.

## Verification Checklist

- [ ] Research brief has question, non-goals, output, and acceptance bar
- [ ] Source packet includes URLs, types, dates when available, takeaways, and confidence
- [ ] Current repo specs/code/task state were checked when the decision affects a project
- [ ] Claude synthesis is source-grounded and includes recommendation, alternatives, MVP scope, risks, and tests
- [ ] Codex adversarial review checked source support and project consistency
- [ ] Review findings were reconciled into the final recommendation before creating docs/tasks
- [ ] Unsupported claims are removed or marked as uncertainty
- [ ] Batch/panel/reporting proposals define missing/failed coverage and aggregation semantics
- [ ] Durable output is written only when useful: `docs/research/`, specs, roadmap, or `TASKS.md`
- [ ] Final report states what Hermes collected, what Claude synthesized, what Codex concluded, what changed after review, and next owner/action
