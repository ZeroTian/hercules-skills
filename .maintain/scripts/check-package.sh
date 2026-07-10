#!/usr/bin/env bash
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
cd "$ROOT"

python3 .maintain/scripts/validate-skill-pack.py --strict
bash -n init.sh .maintain/scripts/smoke-fresh-clone.sh .maintain/scripts/check-package.sh
git diff --check
git diff --cached --check

if git diff --cached --name-only | grep -Ei '(^|/)(\.env|.*secret.*|.*token.*|.*credential.*|id_rsa|id_ed25519|config\.toml)$'; then
  printf 'sensitive staged filename detected\n' >&2
  exit 1
fi

hits=$(git diff --cached --unified=0 --no-color \
  | grep -E '^\+([^+]|$)' \
  | grep -Ein '(BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|api[_-]?key[[:space:]]*[:=]|secret[[:space:]]*[:=]|token[[:space:]]*[:=])' \
  || true)
if [ -n "$hits" ]; then
  printf '%s\n' "$hits" >&2
  exit 1
fi

printf 'maintainer package checks passed\n'
