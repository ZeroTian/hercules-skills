# Governance Document Scope Partition

Use this reference when initializing or refactoring Claude/Codex/Hermes governance in a repository.

## Core rule

README files are for human orientation: what the project is, where to find things, and a short overview of the workflow. Durable agent obligations belong in actor-scoped rule files and task ledgers.

## Recommended artifact roles

| Artifact | Audience | Put here | Do not put here |
|---|---|---|---|
| `README.md` / docs README | Human readers and newcomers | Project overview, navigation, links to rules, short lifecycle summary | Long agent instructions, trigger protocols, SDD/TDD checklists, closure rules |
| `HERMES.md` | Hermes controller | Orchestration duties, actor routing, verification and ledger-update responsibilities, commit/push policy | Project marketing or end-user docs |
| `CLAUDE.md` | Claude Code | Implementation discipline, SDD/TDD, plugin usage, tests, self-check, handoff requirements | Codex closure rules or Hermes process internals beyond what Claude must obey |
| `AGENTS.md` | Codex/agent reviewers | Review scope, CR rules, checkbox truth checks, closure criteria | Claude implementation recipes except as review criteria |
| `TASKS.md` | All actors | Live status, owner/next owner, checkbox plans, task templates, evidence, blocker fields | General project explanation or duplicated long rulebooks |
| `codex-reviews/` | Review history | CR details, findings, recheck evidence, final verdicts | Active task source of truth that conflicts with `TASKS.md` |

## SDD/TDD placement

- Claude execution obligation: `CLAUDE.md`.
- Codex evidence-check obligation: `AGENTS.md`.
- Hermes brief/verification obligation: `HERMES.md` or the Hermes workflow skill.
- Task-level evidence fields and templates: `TASKS.md`.
- README: at most a short sentence such as “Claude/Codex/Hermes rules are in the root actor files.” Do not copy RED/GREEN/REFACTOR or plugin checklists into README.

## Refactor checklist

- [ ] Create or update `HERMES.md` if Hermes orchestration rules are otherwise scattered.
- [ ] Keep README as an index/map and remove long actor-specific rule sections.
- [ ] Ensure `CLAUDE.md`, `AGENTS.md`, and `TASKS.md` carry the detailed obligations.
- [ ] Run a keyword check that workflow-only terms do not remain in README if the project wants a strict separation.
- [ ] Update task records and have Codex independently review the governance refactor when the repo uses a review-required workflow.
