#!/usr/bin/env bash
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
cd "$ROOT"

python3 .maintain/scripts/validate-skill-pack.py --strict
bash -n init.sh .maintain/scripts/smoke-fresh-clone.sh .maintain/scripts/check-package.sh
git diff --check
git diff --cached --check

filename_hits=$(git diff --cached --name-only --diff-filter=ACMR \
  | awk '
      {
        normalized = tolower($0)
        if (normalized ~ /(^|\/)(\.env|.*secret.*|.*token.*|.*credential.*|id_rsa|id_ed25519|config\.toml)$/) {
          printf "redacted category=sensitive-filename path=%s line=- count=1\n", $0
        }
      }
    ')
if [ -n "$filename_hits" ]; then
  printf '%s\n' "$filename_hits" >&2
  exit 1
fi

content_hits=$(git diff --cached --unified=0 --no-color --diff-filter=ACMR \
  | awk '
      function record(category, key) {
        key = category SUBSEP path
        counts[key]++
        lines[key] = lines[key] (lines[key] ? "," : "") new_line
      }
      /^diff --git / { in_hunk = 0; path = ""; next }
      /^\+\+\+ / {
        if ($0 != "+++ /dev/null") {
          path = substr($0, 7)
        }
        next
      }
      /^@@ / {
        split($0, fields, " ")
        range = fields[3]
        sub(/^\+/, "", range)
        split(range, parts, ",")
        new_line = parts[1] + 0
        in_hunk = 1
        next
      }
      in_hunk && /^\+/ {
        content = tolower(substr($0, 2))
        if (content ~ /begin (rsa|openssh|ec) private key/) {
          record("private-key")
        } else if (content ~ /api[_-]?key[[:space:]]*[:=]/) {
          record("api-key")
        } else if (content ~ /secret[[:space:]]*[:=]/) {
          record("secret")
        } else if (content ~ /token[[:space:]]*[:=]/) {
          record("token")
        }
        new_line++
        next
      }
      in_hunk && /^ / { new_line++; next }
      END {
        for (key in counts) {
          split(key, fields, SUBSEP)
          printf "redacted category=%s path=%s line=%s count=%d\n", \
            fields[1], fields[2], lines[key], counts[key]
        }
      }
    ' | sort)
if [ -n "$content_hits" ]; then
  printf '%s\n' "$content_hits" >&2
  exit 1
fi

printf 'maintainer package checks passed\n'
