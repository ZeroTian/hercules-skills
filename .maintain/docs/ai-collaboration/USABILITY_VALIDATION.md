# Usability Validation

Last validated: 2026-07-05 (round 3)

## Verdict

The Hercules skill pack is usable in the current Hermes runtime for the round-3 scope, and clone-copy validation has been practiced against commit `97f78ca` after push.

Validated levels:

1. Runtime symlink and repository layout.
2. Core skill inventory and staged/tracked alignment.
3. Archived candidate safety: candidates are preserved outside runtime loading.
4. Validator and static checks.
5. Bootstrap/dependency doctor in audit-only mode.
6. Actual orchestration practice: Hermes used the skill pack to run Claude implementation, Hermes verification, Codex review, and TASKS closure.
7. Clone-copy validation after commit/push/re-clone for commit `97f78ca` (round 3).

## Practical evidence

### Runtime layout

Commands run:

```bash
readlink -f ~/.hermes/skills/hercules
find skills -mindepth 2 -maxdepth 2 -name SKILL.md | sort
git ls-files 'skills/*/SKILL.md' | sort
find docs/ai-collaboration/candidate-skills -mindepth 2 -maxdepth 2 -name SKILL.md | sort
test ! -e skills/hercules
find skills -type l -print
```

Observed:

- `~/.hermes/skills/hercules` resolves to `/mnt/e/code/hercules-skills/skills`.
- Runtime `skills/` contains the intended 16 core skills (15 after round 2; `skill-pack-governance-validation` added in round 3).
- `git ls-files 'skills/*/SKILL.md'` matches the visible runtime skill files after staging the round-3 promoted core skill.
- No `skills/hercules/` double nesting exists.
- No symlink lives inside `skills/`.
- Archived candidate skills are preserved under `docs/ai-collaboration/candidate-skills/`.

### Skill loading

The following representative core skills loaded successfully through Hermes `skill_view`:

- `hercules-skill-pack-management`
- `workflow-skill-pack-audit`
- `hercules-agent-capability-preflight`
- `coding-agent-orchestration`

Archived candidate safety was also checked:

- `skill_view(name="real-game-closed-loop-validation")` returned `Skill 'real-game-closed-loop-validation' not found`, confirming the archived candidate is not runtime-loaded from `docs/ai-collaboration/candidate-skills/`.

### Validator and static checks

Commands run:

```bash
python3 scripts/validate-skill-pack.py
git diff --check
bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
```

Observed:

```text
errors:    0
warnings:  0
signals:   0
exit code: 0
```

`git diff --check` passed.

`bash -n` for the bootstrap script passed.

### Bootstrap/dependency doctor

Command run:

```bash
HERCULES_CHECK_ONLY=1 bash skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
```

Observed:

- Claude Code present: `2.1.201`.
- Codex CLI present: `0.142.5`.
- Required external Hermes skills present:
  - `subagent-driven-development`
  - `writing-plans`
- Required Claude plugin marketplaces present:
  - `claude-plugins-official`
  - `omc`
- Required Claude plugins present:
  - `superpowers`
  - `oh-my-claudecode`
- Relevant MCP/plugin capability checks completed.
- Script exited successfully.

### Real workflow practice already performed

This skill pack was not only statically validated. It was used in the current repository workflow:

1. `hercules-agent-capability-preflight` pattern was used to scan Claude/Codex versions, plugins, MCP servers, and effort settings.
2. `workflow-skill-pack-audit` guided the round-2 reconciliation:
   - inventory runtime/tracked skills;
   - promote two core skills;
   - archive four non-core candidates;
   - update README/ARCHITECTURE/SKILL_GROUP_AUDIT/TASKS;
   - validate to zero warnings.
3. `hercules-skill-pack-management` rules were exercised:
   - flat `skills/<skill>/SKILL.md` layout;
   - runtime symlink target checked;
   - no double nesting;
   - archived candidates outside runtime loading.
4. `coding-agent-orchestration` pattern was exercised:
   - Claude Code performed the reconciliation implementation;
   - Hermes verified the result with real commands;
   - Codex CLI performed independent final review;
   - Hermes saved the Codex review and closed TASKS entries.
5. `scripts/validate-skill-pack.py` caught and cleared reconciliation warnings after staged core alignment.

Codex final review record:

```text
docs/ai-collaboration/codex-reviews/2026-07-05-round2-skill-pack-reconciliation.md
```

Codex verdict:

```text
PASS, highest severity: none
```

### Clone-copy validation (commit 97f78ca)

After commit `97f78ca` was pushed to `origin/main`, a clone-copy acceptance test was performed to confirm the pack survives a fresh clone and loads cleanly outside the active-development tree. This closes the round-2 gaps "Clone-copy install from GitHub after committing/pushing" and "Full commit/push/re-clone acceptance loop."

Commands run:

```bash
rm -rf /tmp/hercules-skills-smoke
mkdir -p /tmp/hercules-skills-smoke
git clone https://github.com/ZeroTian/hercules-skills.git /tmp/hercules-skills-smoke/hercules-skills
cd /tmp/hercules-skills-smoke/hercules-skills
git rev-parse HEAD
python3 scripts/validate-skill-pack.py
HERCULES_CHECK_ONLY=1 bash skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
```

Observed:

- Cloned HEAD: `97f78cacbc107f02b918576fdddc053388eab95d` (matches `97f78ca`).
- Validator: 0 errors, 0 warnings, 0 reflection signals, exit 0.
- Bootstrap audit-only: `[hercules-bootstrap] done`.

This practice is now codified by the `skill-pack-governance-validation` core skill (round-3 promotion), which turns "the files look right" into evidence that the pack is usable in the current runtime and safe to package. The clone at `97f78ca` reflects the 15-skill committed state (the round-3 skill is untracked locally and not yet in that clone); a follow-up clone-copy run is recommended after the round-3 commit is pushed.

## Not yet covered

The following are not yet fully practiced:

1. Fresh-machine migration from a clean Hermes install.
2. A new external project initialized from scratch using the finalized skill pack.
3. Clone-copy acceptance for the round-3 commit (the `97f78ca` clone-copy covered the 15-skill committed state; the round-3 skill `skill-pack-governance-validation` is untracked locally and not yet in that clone).

These should be validated after the user approves commit/push of the round-3 promotion.

## Next recommended validation

The clone-style acceptance test has been practiced for commit `97f78ca` (see "Clone-copy validation" above). After the round-3 promotion is committed and pushed, re-run the same clone-style acceptance test to confirm the 16-skill pack survives a fresh clone:

```bash
rm -rf /tmp/hercules-skills-smoke
mkdir -p /tmp/hercules-skills-smoke
git clone https://github.com/ZeroTian/hercules-skills.git /tmp/hercules-skills-smoke/hercules-skills
cd /tmp/hercules-skills-smoke/hercules-skills
git rev-parse HEAD
python3 scripts/validate-skill-pack.py
HERCULES_CHECK_ONLY=1 bash skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh
```

Then start a fresh Hermes session and confirm representative skill loading (including `skill-pack-governance-validation`) from the cloned pack. The remaining uncovered level is fresh-machine migration from a clean Hermes install.
