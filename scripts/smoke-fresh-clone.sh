#!/usr/bin/env bash
set -euo pipefail

SOURCE_ROOT=$(git rev-parse --show-toplevel)
KEEP_TMP=${HERCULES_SMOKE_KEEP_TMP:-0}
TMP_DIR=$(mktemp -d -t hercules-fresh-clone.XXXXXX)

cleanup() {
  if [ "$KEEP_TMP" != "1" ]; then
    rm -rf "$TMP_DIR"
  else
    printf '[hercules-smoke] kept temp dir: %s\n' "$TMP_DIR" >&2
  fi
}
trap cleanup EXIT

log() { printf '[hercules-smoke] %s\n' "$*"; }

CLONE_DIR="$TMP_DIR/repo"
log "source: $SOURCE_ROOT"
log "clone: $CLONE_DIR"

git clone --quiet --no-hardlinks "$SOURCE_ROOT" "$CLONE_DIR"

# Apply the candidate staged package to the temporary clone without mutating the
# source repository. Untracked files must be staged by the caller if they are
# part of the package under test. Unstaged tracked diffs are ignored by default
# so the smoke cannot pass because of files that would not be committed.
if ! git -C "$SOURCE_ROOT" diff --cached --quiet --binary; then
  log "applying staged diff to clone"
  git -C "$SOURCE_ROOT" diff --cached --binary | git -C "$CLONE_DIR" apply --index --binary
fi

if [ "${HERCULES_SMOKE_INCLUDE_UNSTAGED:-0}" = "1" ]; then
  if ! git -C "$SOURCE_ROOT" diff --quiet --binary; then
    log "applying unstaged tracked diff to clone (explicit opt-in)"
    git -C "$SOURCE_ROOT" diff --binary | git -C "$CLONE_DIR" apply --binary
  fi
elif ! git -C "$SOURCE_ROOT" diff --quiet --binary; then
  log "ignoring unstaged tracked diff; set HERCULES_SMOKE_INCLUDE_UNSTAGED=1 to include it"
fi

log "running validator"
python3 "$CLONE_DIR/scripts/validate-skill-pack.py"

if [ -x "$CLONE_DIR/scripts/hercules" ]; then
  log "running scripts/hercules validate"
  "$CLONE_DIR/scripts/hercules" validate
else
  log "scripts/hercules not executable in clone; skipping helper validation"
fi

log "running bootstrap syntax check"
bash -n "$CLONE_DIR/skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh"

log "fresh-clone smoke passed"
