#!/usr/bin/env bash
set -euo pipefail

REPO_URL=${HERCULES_REPO_URL:-https://github.com/ZeroTian/hercules-skills.git}
BRANCH=${HERCULES_BRANCH:-main}
HERCULES_HOME=${HERCULES_HOME:-$HOME/.hercules}
HERMES_HOME=${HERMES_HOME:-$HOME/.hermes}

die() { printf 'Hercules init: %s\n' "$*" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }

have git || die "Git is required but was not found. Install Git using its official instructions, then rerun init."
have hermes || die "Hermes is required but was not found. Install Hermes using its official instructions, then rerun init."

EXPECTED_SOURCE="$HERCULES_HOME/skills"
if [ -d "$EXPECTED_SOURCE" ]; then
  EXPECTED_SOURCE=$(cd "$EXPECTED_SOURCE" && pwd -P)
fi
RUNTIME="$HERMES_HOME/skills/hercules"
if [ -L "$RUNTIME" ]; then
  [ "$(readlink "$RUNTIME")" = "$EXPECTED_SOURCE" ] || die "$RUNTIME is an unrelated symlink; no files were changed."
elif [ -e "$RUNTIME" ]; then
  die "$RUNTIME already exists and was preserved; move it manually before rerunning init."
fi

if [ -d "$HERCULES_HOME/.git" ]; then
  git -C "$HERCULES_HOME" fetch origin "$BRANCH"
  git -C "$HERCULES_HOME" merge --ff-only "origin/$BRANCH"
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
