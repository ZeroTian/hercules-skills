#!/usr/bin/env bash
set -euo pipefail

REPO_URL=${HERCULES_REPO_URL:-https://github.com/ZeroTian/hercules-skills.git}
BRANCH=${HERCULES_BRANCH:-main}
HERCULES_HOME=${HERCULES_HOME:-$HOME/.hercules}
HERMES_HOME=${HERMES_HOME:-$HOME/.hermes}

die() { printf 'Hercules init: %s\n' "$*" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }
require_directory_ancestors() {
  local path=$1 parent
  while [ "$path" != "/" ] && [ "$path" != "." ]; do
    if { [ -e "$path" ] || [ -L "$path" ]; } && [ ! -d "$path" ]; then
      die "$path blocks the Hermes runtime path and was preserved; no files were changed."
    fi
    parent=$(dirname "$path")
    [ "$parent" != "$path" ] || break
    path=$parent
  done
}

have git || die "Git is required but was not found. Hercules 未安装或修改任何内容。 Official Git documentation: https://git-scm.com/downloads"
have hermes || die "Hermes is required but was not found. Hercules 未安装或修改任何内容。 Official Hermes documentation: https://hermes-agent.nousresearch.com/docs/getting-started/quickstart"

EXPECTED_SOURCE="$HERCULES_HOME/skills"
if [ -d "$EXPECTED_SOURCE" ]; then
  EXPECTED_SOURCE=$(cd "$EXPECTED_SOURCE" && pwd -P)
fi
RUNTIME="$HERMES_HOME/skills/hercules"
require_directory_ancestors "$(dirname "$RUNTIME")"
if [ -L "$RUNTIME" ]; then
  [ "$(readlink "$RUNTIME")" = "$EXPECTED_SOURCE" ] || die "$RUNTIME is an unrelated symlink; no files were changed."
elif [ -e "$RUNTIME" ]; then
  die "$RUNTIME already exists and was preserved; move it manually before rerunning init."
fi

if [ -e "$HERCULES_HOME/.git" ]; then
  ORIGIN_URL=$(git -C "$HERCULES_HOME" remote get-url origin 2>/dev/null) ||
    die "$HERCULES_HOME is not a Hercules Git checkout with an origin; no files were changed."
  [ "$ORIGIN_URL" = "$REPO_URL" ] ||
    die "$HERCULES_HOME origin does not match the configured Hercules repository; no files were changed."
  CURRENT_BRANCH=$(git -C "$HERCULES_HOME" symbolic-ref --quiet --short HEAD 2>/dev/null) ||
    die "$HERCULES_HOME is not on the configured Hercules branch; no files were changed."
  [ "$CURRENT_BRANCH" = "$BRANCH" ] ||
    die "$HERCULES_HOME is on branch $CURRENT_BRANCH, expected $BRANCH; no files were changed."
  [ -z "$(git -C "$HERCULES_HOME" status --porcelain=v1 --untracked-files=all)" ] || die "$HERCULES_HOME has local changes; no files were changed."
  LOCAL_HEAD=$(git -C "$HERCULES_HOME" rev-parse HEAD) || die "$HERCULES_HOME HEAD could not be inspected; no files were changed."
  TRACKING_REF="refs/remotes/origin/$BRANCH"
  TRACKING_HEAD=$(git -C "$HERCULES_HOME" rev-parse --verify "$TRACKING_REF" 2>/dev/null || true)
  PREFLIGHT_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/hercules-init.XXXXXX") || die "a temporary Git preflight directory could not be created; no files were changed."
  PREFLIGHT_REPO="$PREFLIGHT_ROOT/repository"
  cleanup_preflight() { rm -rf "$PREFLIGHT_ROOT"; }
  trap cleanup_preflight EXIT HUP INT TERM
  git clone --quiet --no-checkout --single-branch --branch "$BRANCH" "$REPO_URL" "$PREFLIGHT_REPO" || die "the configured Hercules branch could not be inspected; no files were changed."
  REMOTE_HEAD=$(git -C "$PREFLIGHT_REPO" rev-parse HEAD) || die "the configured Hercules branch has no inspectable HEAD; no files were changed."
  git -C "$PREFLIGHT_REPO" fetch --quiet "$HERCULES_HOME" "refs/heads/$BRANCH:refs/hercules-preflight/local" || die "$HERCULES_HOME local branch could not be inspected; no files were changed."
  if [ -n "$TRACKING_HEAD" ]; then
    git -C "$PREFLIGHT_REPO" fetch --quiet "$HERCULES_HOME" "$TRACKING_REF:refs/hercules-preflight/tracking" || die "$HERCULES_HOME remote-tracking branch could not be inspected; no files were changed."
    git -C "$PREFLIGHT_REPO" merge-base --is-ancestor "$TRACKING_HEAD" "$REMOTE_HEAD" || die "$HERCULES_HOME remote history was rewritten; no files were changed."
  fi
  git -C "$PREFLIGHT_REPO" merge-base --is-ancestor "$LOCAL_HEAD" "$REMOTE_HEAD" || die "$HERCULES_HOME does not fast-forward to origin/$BRANCH; no files were changed."
  git -C "$HERCULES_HOME" fetch --quiet --no-write-fetch-head "$PREFLIGHT_REPO" "refs/heads/$BRANCH"
  [ -z "$(git -C "$HERCULES_HOME" status --porcelain=v1 --untracked-files=all)" ] || die "$HERCULES_HOME changed during preflight; refs and worktree were preserved."
  git -C "$HERCULES_HOME" merge-base --is-ancestor HEAD "$REMOTE_HEAD" || die "$HERCULES_HOME changed during preflight; refs and worktree were preserved."
  git -C "$HERCULES_HOME" merge --ff-only "$REMOTE_HEAD"
  if [ -n "$TRACKING_HEAD" ]; then
    git -C "$HERCULES_HOME" update-ref "$TRACKING_REF" "$REMOTE_HEAD" "$TRACKING_HEAD"
  else
    git -C "$HERCULES_HOME" update-ref "$TRACKING_REF" "$REMOTE_HEAD"
  fi
  cleanup_preflight
  trap - EXIT HUP INT TERM
elif [ -e "$HERCULES_HOME" ]; then
  die "$HERCULES_HOME exists but is not a Hercules Git checkout; no files were changed."
else
  mkdir -p "$(dirname "$HERCULES_HOME")"
  git clone --branch "$BRANCH" "$REPO_URL" "$HERCULES_HOME"
fi

SOURCE=$(cd "$HERCULES_HOME/skills" && pwd -P)
mkdir -p "$(dirname "$RUNTIME")"

if [ -L "$RUNTIME" ]; then
  [ "$(readlink "$RUNTIME")" = "$SOURCE" ] || die "$RUNTIME no longer points to the installed Skills."
else
  ln -s "$SOURCE" "$RUNTIME"
fi

printf 'Hercules Skills are ready.\n'
printf '1. hermes --tui\n'
printf '2. /skill hercules\n'
