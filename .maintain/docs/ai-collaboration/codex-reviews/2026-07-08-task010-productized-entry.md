# Codex Review — TASK-010 productized entry + README landing

Date: 2026-07-08
Reviewer: Codex CLI (`codex exec`, model `gpt-5.5`, reasoning effort `xhigh`)
Scope: staged TASK-010 package: `scripts/hercules`, README landing, TASKS/roadmap state.

## Initial verdict

FAIL; highest severity P1.

### CR-T010-001 — P1 — `scripts/hercules` staged as non-executable

Finding: README documents direct execution via `scripts/hercules ...`, but the staged script mode was `100644`, so a fresh POSIX clone would not be able to run the quickstart directly.

Fix: Hermes staged executable mode with `git update-index --chmod=+x scripts/hercules`; staged mode then showed `100755`.

### CR-T010-002 — P2 — secret scan wrote hits to fixed `/tmp` path

Finding: the staged privacy scan redirected matched secret lines to `/tmp/hercules_staged_secret_hits.txt` before printing them. If a real token were staged, the helper would persist it in a predictable temp path.

Fix: Hermes replaced the fixed temp-file redirect with an in-memory `hits=$(... || true)` variable and prints only the first 20 hits on failure. `git grep --cached -n '/tmp/hercules_staged_secret_hits' -- scripts/hercules` returned no matches.

## Recheck verdict

PASS. Codex verified:

- `git ls-files -s scripts/hercules` reports `100755`;
- `git diff --cached --summary -- scripts/hercules` reports `create mode 100755 scripts/hercules`;
- the staged privacy scan no longer references `/tmp/hercules_staged_secret_hits`;
- no remaining issues for CR-T010-001 or CR-T010-002.

```json
{"verdict":"PASS","highest_severity":"none","findings":[],"next_owner":"none"}
```
