#!/usr/bin/env bash
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
cd "$ROOT"

python3 .maintain/scripts/validate-skill-pack.py --strict
bash -n init.sh .maintain/scripts/smoke-fresh-clone.sh .maintain/scripts/check-package.sh

redacted_diff_check() {
  local diff_check_output diff_check_hits
  if diff_check_output=$(git diff "$@" --check 2>&1); then
    return 0
  fi

  diff_check_hits=$(printf '%s\n' "$diff_check_output" \
    | awk '
        function record(category, path, line, key) {
          key = category SUBSEP path
          counts[key]++
          lines[key] = lines[key] (lines[key] ? "," : "") line
        }
        {
          if (skip_raw_line) {
            skip_raw_line = 0
            next
          }

          header = $0
          remaining = header
          offset = 0
          marker_position = 0
          marker = ""
          while (match(remaining, /:[0-9]+: /)) {
            marker_position = offset + RSTART
            marker = substr(remaining, RSTART, RLENGTH)
            offset += RSTART + RLENGTH - 1
            remaining = substr(remaining, RSTART + RLENGTH)
          }

          if (!marker_position) {
            unknown_count++
            next
          }

          path = substr(header, 1, marker_position - 1)
          line = marker
          gsub(/[^0-9]/, "", line)
          message = tolower(substr(header, marker_position + length(marker)))
          if (message ~ /^trailing whitespace/) {
            category = "trailing-whitespace"
          } else if (message ~ /^space before tab in indent/) {
            category = "space-before-tab"
          } else if (message ~ /^new blank line at eof/) {
            category = "blank-line-at-eof"
          } else if (message ~ /^leftover conflict marker/) {
            category = "conflict-marker"
          } else {
            category = "diff-check"
          }
          record(category, path, line)
          skip_raw_line = 1
        }
        END {
          for (key in counts) {
            split(key, fields, SUBSEP)
            printf "redacted category=%s path=%s line=%s count=%d\n", \
              fields[1], fields[2], lines[key], counts[key]
          }
          if (unknown_count) {
            printf "redacted category=diff-check path=- line=- count=%d\n", \
              unknown_count
          }
        }
      ' | sort)
  if [ -z "$diff_check_hits" ]; then
    diff_check_hits='redacted category=diff-check path=- line=- count=1'
  fi
  printf '%s\n' "$diff_check_hits" >&2
  return 1
}

redacted_diff_check
redacted_diff_check --cached

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
