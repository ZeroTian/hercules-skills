#!/usr/bin/env bash
set -euo pipefail

# Bootstrap/check runtime dependencies for the portable Hercules Hermes workflow.
# Safe defaults:
# - Installs missing CLI packages with npm global install.
# - Installs missing Hermes hub skills.
# - Installs/enables Claude plugin marketplaces/plugins only when HERCULES_INSTALL_OPTIONAL=1.
# - Does not inspect or modify third-party provider/authentication state.
# - Prints deep plugin/MCP/feature inventories only with HERCULES_VERBOSE=1.
#
# Env knobs:
#   HERCULES_YES=1              run installs without prompting
#   HERCULES_CHECK_ONLY=1       only report, do not install
#   HERCULES_SKIP_REGISTRY=1    do not change npm/pnpm registry
#   HERCULES_INSTALL_OPTIONAL=1 install Claude plugins/marketplaces too
#                              (superpowers, oh-my-claudecode, playwright, context7, pyright-lsp, codex@openai-codex)
#   HERCULES_VERBOSE=1          print deep plugin/MCP/feature inventories

YES=${HERCULES_YES:-0}
CHECK_ONLY=${HERCULES_CHECK_ONLY:-0}
SKIP_REGISTRY=${HERCULES_SKIP_REGISTRY:-0}
INSTALL_OPTIONAL=${HERCULES_INSTALL_OPTIONAL:-0}
VERBOSE=${HERCULES_VERBOSE:-0}
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
    log "PLAN: $*"
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
    if [ "$CHECK_ONLY" = "1" ]; then
      log "PLAN: set npm registry to $NPM_REGISTRY"
      if have_cmd pnpm; then log "PLAN: set pnpm registry to $NPM_REGISTRY"; fi
      return 0
    fi
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

latest_dir() {
  # Print the lexically last matching directory. This is only a best-effort
  # cache inspection helper; plugin managers remain the source of truth.
  find "$1" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort | tail -1
}

report_plugin_deep_inventory() {
  log "Plugin deep capability inventory"

  local omc_root=""
  if [ -d "$HOME/.claude/plugins/cache/omc/oh-my-claudecode" ]; then
    omc_root=$(latest_dir "$HOME/.claude/plugins/cache/omc/oh-my-claudecode")
  fi
  if [ -n "$omc_root" ] && [ -d "$omc_root" ]; then
    log "OMC root: $omc_root"
    if [ -f "$omc_root/commands/omc-teams.md" ] || [ -f "$omc_root/skills/omc-teams/SKILL.md" ]; then
      log "OMC team capability: present"
    else
      warn "OMC team capability not confirmed from commands/omc-teams.md or skills/omc-teams/SKILL.md"
    fi
    printf '[hercules-bootstrap] OMC agents: '
    find "$omc_root/agents" -maxdepth 1 -name '*.md' -type f 2>/dev/null | sed 's|.*/||; s|\.md$||' | sort | paste -sd ',' - || true
    printf '[hercules-bootstrap] OMC commands: '
    find "$omc_root/commands" -maxdepth 1 -name '*.md' -type f 2>/dev/null | sed 's|.*/||; s|\.md$||' | sort | paste -sd ',' - || true
    printf '[hercules-bootstrap] OMC bundled skills: '
    find "$omc_root/skills" -mindepth 2 -maxdepth 2 -name 'SKILL.md' -type f 2>/dev/null | sed 's|.*/skills/||; s|/SKILL.md$||' | sort | paste -sd ',' - || true
  else
    warn "OMC plugin cache not found for deep inventory"
  fi

  local sp_root=""
  if [ -d "$HOME/.claude/plugins/cache/claude-plugins-official/superpowers" ]; then
    sp_root=$(latest_dir "$HOME/.claude/plugins/cache/claude-plugins-official/superpowers")
  fi
  if [ -n "$sp_root" ] && [ -d "$sp_root" ]; then
    log "Superpowers root: $sp_root"
    printf '[hercules-bootstrap] Superpowers bundled skills: '
    find "$sp_root/skills" -mindepth 2 -maxdepth 2 -name 'SKILL.md' -type f 2>/dev/null | sed 's|.*/skills/||; s|/SKILL.md$||' | sort | paste -sd ',' - || true
  else
    warn "Superpowers plugin cache not found for deep inventory"
  fi

  # OpenAI codex-plugin-cc is an optional external Claude plugin. When present,
  # inventory its /codex:* slash commands and the codex-rescue agent. Absent
  # files are warnings only — the plugin is optional and never auto-installed.
  local codex_cc_root=""
  if [ -d "$HOME/.claude/plugins/cache/openai-codex/codex" ]; then
    codex_cc_root=$(latest_dir "$HOME/.claude/plugins/cache/openai-codex/codex")
  fi
  if [ -n "$codex_cc_root" ] && [ -d "$codex_cc_root" ]; then
    log "Codex CC plugin root: $codex_cc_root"
    printf '[hercules-bootstrap] Codex plugin /codex:* commands: '
    find "$codex_cc_root/commands" -maxdepth 1 -name '*.md' -type f 2>/dev/null | sed 's|.*/||; s|\.md$||; s|^|/codex:|' | sort | paste -sd ',' - || true
    if [ -f "$codex_cc_root/agents/codex-rescue.md" ]; then
      log "Codex plugin codex-rescue agent: present (codex:codex-rescue)"
    else
      warn "Codex plugin codex-rescue agent not found at agents/codex-rescue.md (write-capable rescue unavailable)"
    fi
  else
    warn "Codex Claude plugin cache not found for deep inventory (optional; install with HERCULES_INSTALL_OPTIONAL=1)"
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
    if [ "$INSTALL_OPTIONAL" = "1" ]; then
      ensure_marketplace claude-plugins-official anthropics/claude-plugins-official || true
      ensure_marketplace omc https://github.com/Yeachan-Heo/oh-my-claudecode.git || true
      # openai/codex-plugin-cc registers the marketplace under the stable name
      # "openai-codex"; the plugin is referenced as codex@openai-codex.
      ensure_marketplace openai-codex openai/codex-plugin-cc || true
      ensure_claude_plugin superpowers@claude-plugins-official superpowers || true
      ensure_claude_plugin oh-my-claudecode@omc oh-my-claudecode || true
      ensure_claude_plugin playwright@claude-plugins-official playwright || true
      ensure_claude_plugin context7@claude-plugins-official context7 || true
      ensure_claude_plugin pyright-lsp@claude-plugins-official pyright-lsp || true
      ensure_claude_plugin codex@openai-codex codex || true
    else
      log "skipping Claude plugin marketplace/plugin installs (set HERCULES_INSTALL_OPTIONAL=1 to align plugin dependencies)"
    fi
  fi

  if [ "$VERBOSE" = "1" ]; then
    report_capabilities
    report_plugin_deep_inventory
  else
    log "deep capability inventory skipped (set HERCULES_VERBOSE=1 for troubleshooting)"
  fi
  log "provider access not probed; authentication remains user-managed"
  log "done"
}

main "$@"
