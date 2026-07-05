#!/usr/bin/env bash
set -euo pipefail

# Bootstrap/check runtime dependencies for the portable Hercules Hermes workflow.
# Safe defaults:
# - Installs missing CLI packages with npm global install.
# - Installs missing Hermes hub skills.
# - Adds Claude plugin marketplaces if absent, then installs/enables required plugins.
# - Does not perform interactive auth; reports required login commands instead.
#
# Env knobs:
#   HERCULES_YES=1              run installs without prompting
#   HERCULES_CHECK_ONLY=1       only report, do not install
#   HERCULES_SKIP_REGISTRY=1    do not change npm/pnpm registry
#   HERCULES_INSTALL_OPTIONAL=1 install optional plugins too

YES=${HERCULES_YES:-0}
CHECK_ONLY=${HERCULES_CHECK_ONLY:-0}
SKIP_REGISTRY=${HERCULES_SKIP_REGISTRY:-0}
INSTALL_OPTIONAL=${HERCULES_INSTALL_OPTIONAL:-0}
NPM_REGISTRY=${NPM_REGISTRY:-https://registry.npmmirror.com}

log() { printf '[hercules-bootstrap] %s\n' "$*"; }
warn() { printf '[hercules-bootstrap][warn] %s\n' "$*" >&2; }
need_install() { [ "$CHECK_ONLY" != "1" ]; }

confirm() {
  if [ "$YES" = "1" ]; then return 0; fi
  printf '%s [y/N] ' "$*" >&2
  read -r ans || true
  case "${ans:-}" in y|Y|yes|YES) return 0 ;; *) return 1 ;; esac
}

run_install() {
  if [ "$CHECK_ONLY" = "1" ]; then
    log "CHECK_ONLY: would run: $*"
    return 0
  fi
  if [ "$YES" = "1" ] || confirm "Run: $* ?"; then
    "$@"
  else
    warn "skipped: $*"
  fi
}

have_cmd() { command -v "$1" >/dev/null 2>&1; }

ensure_node_toolchain() {
  if ! have_cmd npm; then
    warn "npm is missing. Install Node.js/npm first, then rerun this script."
    return 1
  fi
  if [ "$SKIP_REGISTRY" != "1" ]; then
    npm config set registry "$NPM_REGISTRY" >/dev/null || true
    if have_cmd pnpm; then pnpm config set registry "$NPM_REGISTRY" >/dev/null || true; fi
  fi
}

ensure_cli() {
  local cmd="$1" pkg="$2"
  if have_cmd "$cmd"; then
    log "$cmd present: $($cmd --version 2>/dev/null | head -1 || true)"
    return 0
  fi
  warn "$cmd missing"
  ensure_node_toolchain || return 1
  run_install npm install -g "$pkg"
  if have_cmd "$cmd"; then
    log "$cmd installed: $($cmd --version 2>/dev/null | head -1 || true)"
  else
    warn "$cmd still missing after install attempt"
    return 1
  fi
}

skill_installed() {
  local name="$1"
  local hhome="${HERMES_HOME:-$HOME/.hermes}"
  if find "$hhome/skills" -path "*/$name/SKILL.md" -print -quit 2>/dev/null | grep -q .; then
    return 0
  fi
  hermes skills list 2>/dev/null | grep -q "$name"
}

ensure_skill() {
  local name="$1" identifier="$2"
  if ! have_cmd hermes; then
    warn "hermes command missing; install Hermes first. Cannot install skill $name."
    return 1
  fi
  if skill_installed "$name"; then
    log "Hermes skill present: $name"
    return 0
  fi
  warn "Hermes skill missing: $name"
  run_install hermes skills install "$identifier"
}

marketplace_present() {
  claude plugins marketplace list 2>/dev/null | grep -q "❯ $1\b\| $1\b"
}

ensure_marketplace() {
  local name="$1" source="$2"
  if ! have_cmd claude; then
    warn "claude missing; cannot add marketplace $name"
    return 1
  fi
  if marketplace_present "$name"; then
    log "Claude marketplace present: $name"
    return 0
  fi
  warn "Claude marketplace missing: $name"
  run_install claude plugins marketplace add "$source"
}

plugin_present() {
  local plugin="$1"
  claude plugins list 2>/dev/null | grep -q "$plugin@"
}

ensure_claude_plugin() {
  local plugin_id="$1" display="$2"
  if ! have_cmd claude; then
    warn "claude missing; cannot install plugin $display"
    return 1
  fi
  if plugin_present "$display"; then
    log "Claude plugin present: $display"
    return 0
  fi
  warn "Claude plugin missing: $display"
  run_install claude plugins install --scope user "$plugin_id"
  # Enable if installed but disabled.
  if plugin_present "$display"; then
    claude plugins enable "$display" >/dev/null 2>&1 || true
  fi
}

report_auth() {
  log "Auth status checks"
  if have_cmd claude; then
    claude auth status --text 2>/dev/null || warn "Claude auth not ready. Run: claude auth login --console or run claude once interactively."
  fi
  if have_cmd codex; then
    codex login status 2>/dev/null || warn "Codex auth not ready. Run: codex login"
  fi
}

report_capabilities() {
  log "Capability summary"
  if have_cmd claude; then
    claude --version || true
    claude plugins list 2>/dev/null | sed -n '1,160p' || true
    claude mcp list 2>/dev/null | sed -n '1,160p' || true
  fi
  if have_cmd codex; then
    codex --version || true
    codex mcp list 2>/dev/null | sed -n '1,160p' || true
    codex features list 2>/dev/null | sed -n '1,120p' || true
  fi
}

main() {
  log "starting Hercules workflow bootstrap (check_only=$CHECK_ONLY yes=$YES)"

  ensure_node_toolchain || true
  ensure_cli claude '@anthropic-ai/claude-code' || true
  ensure_cli codex '@openai/codex' || true

  ensure_skill subagent-driven-development official/software-development/subagent-driven-development || true
  ensure_skill writing-plans skills-sh/obra/superpowers/writing-plans || true

  if have_cmd claude; then
    ensure_marketplace claude-plugins-official anthropics/claude-plugins-official || true
    ensure_marketplace omc https://github.com/Yeachan-Heo/oh-my-claudecode.git || true
    ensure_claude_plugin superpowers@claude-plugins-official superpowers || true
    ensure_claude_plugin oh-my-claudecode@omc oh-my-claudecode || true
    if [ "$INSTALL_OPTIONAL" = "1" ]; then
      ensure_claude_plugin playwright@claude-plugins-official playwright || true
      ensure_claude_plugin context7@claude-plugins-official context7 || true
      ensure_claude_plugin pyright-lsp@claude-plugins-official pyright-lsp || true
    fi
  fi

  report_auth
  report_capabilities
  log "done"
}

main "$@"
