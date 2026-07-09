#!/usr/bin/env bash
set -euo pipefail

# One-command installer for the Hercules Hermes skill pack.
# Safe defaults:
# - Installs/checks OS basics, Hermes, Claude Code CLI, Codex CLI, required skills/plugins.
# - Installs Hercules by symlinking ~/.hermes/skills/hercules -> <repo>/skills.
# - Does not automate interactive auth; prints claude/codex/hermes login/setup commands.
# - Optional token-spending/state-changing Claude plugins are installed only with --optional.

REPO_URL=${HERCULES_REPO_URL:-https://github.com/ZeroTian/hercules-skills.git}
BRANCH=${HERCULES_BRANCH:-main}
REPO_DIR=${HERCULES_REPO_DIR:-$HOME/code/hercules-skills}
INSTALL_MODE=${HERCULES_INSTALL_MODE:-symlink} # symlink|copy
REPO_DIR_EXPLICIT=0
YES=${HERCULES_YES:-0}
CHECK_ONLY=${HERCULES_CHECK_ONLY:-0}
INSTALL_OPTIONAL=${HERCULES_INSTALL_OPTIONAL:-0}
SKIP_OS_PACKAGES=${HERCULES_SKIP_OS_PACKAGES:-0}
SKIP_HERMES_INSTALL=${HERCULES_SKIP_HERMES_INSTALL:-0}
SKIP_BOOTSTRAP=${HERCULES_SKIP_BOOTSTRAP:-0}
NPM_REGISTRY=${NPM_REGISTRY:-https://registry.npmmirror.com}

log() { printf '[hercules-install] %s\n' "$*"; }
warn() { printf '[hercules-install][warn] %s\n' "$*" >&2; }
die() { printf '[hercules-install][error] %s\n' "$*" >&2; exit 1; }
have_cmd() { command -v "$1" >/dev/null 2>&1; }

usage() {
  cat <<'USAGE'
Hercules one-command installer

Usage:
  scripts/install-hercules.sh [options]
  curl -fsSL https://raw.githubusercontent.com/ZeroTian/hercules-skills/main/scripts/install-hercules.sh | bash -s -- [options]

Product modes:
  --full                 Non-interactive recommended setup; includes optional Claude plugins.
  --minimal              Non-interactive minimal setup; no Claude plugin mutation.
  --dry-run              Alias for --check. Preview only; no installs/clones/pulls/config/symlink writes.
  --check, --check-only  Audit-only mode. Report what would happen; do not mutate the machine.

Compatibility / advanced options:
  -y, --yes              Non-interactive install where possible.
  --optional             Also install optional Claude plugins (superpowers, oh-my-claudecode, playwright, context7, pyright-lsp, codex@openai-codex).
  --copy                 Copy skills into ~/.hermes/skills/hercules instead of symlinking to the repo.
  --symlink              Symlink ~/.hermes/skills/hercules to <repo>/skills (default).
  --repo-url URL         Git repository URL. Default: https://github.com/ZeroTian/hercules-skills.git
  --branch NAME          Branch to clone/pull. Default: main.
  --repo-dir DIR         Local checkout directory. Default: ~/code/hercules-skills.
  --skip-os-packages     Do not install OS packages with apt/brew.
  --skip-hermes-install  Do not run the official Hermes installer if hermes is missing.
  --skip-bootstrap       Do not run Hercules dependency bootstrap after installing skills.
  -h, --help             Show this help.

No options:
  Starts a small interactive setup picker when /dev/tty is available.
  In non-interactive contexts, pass --full --yes, --minimal --yes, or --dry-run.

Environment knobs:
  HERCULES_REPO_URL, HERCULES_BRANCH, HERCULES_REPO_DIR, HERCULES_INSTALL_MODE
  HERCULES_YES=1, HERCULES_CHECK_ONLY=1, HERCULES_INSTALL_OPTIONAL=1
  HERCULES_SKIP_OS_PACKAGES=1, HERCULES_SKIP_HERMES_INSTALL=1, HERCULES_SKIP_BOOTSTRAP=1
  NPM_REGISTRY=https://registry.npmmirror.com

This script cannot complete interactive auth. If needed, run after install:
  hermes setup
  claude auth login --console
  codex login
USAGE
}

read_tty() {
  if [ -r /dev/tty ]; then
    read -r "$1" </dev/tty || true
  else
    read -r "$1" || true
  fi
}

confirm() {
  if [ "$YES" = "1" ]; then return 0; fi
  printf '%s [y/N] ' "$*" >&2
  local ans=""
  read_tty ans
  case "${ans:-}" in y|Y|yes|YES) return 0 ;; *) return 1 ;; esac
}

prompt_setup_mode() {
  if [ ! -r /dev/tty ]; then
    usage >&2
    die "no options supplied and no TTY available; use --full --yes, --minimal --yes, or --dry-run"
  fi

  cat >/dev/tty <<'EOF'
Hercules setup

Choose setup mode:
  1) Full recommended setup  (install optional Claude plugins too)
  2) Minimal setup           (no Claude plugin mutation)
  3) Dry run only            (preview, no writes)
  4) Custom flags            (abort and rerun with explicit options)
EOF
  printf 'Select [1/2/3/4]: ' >/dev/tty
  local choice=""
  read_tty choice
  case "${choice:-}" in
    1) YES=1; INSTALL_OPTIONAL=1 ;;
    2) YES=1; INSTALL_OPTIONAL=0 ;;
    3) CHECK_ONLY=1 ;;
    4) usage; exit 0 ;;
    *) die "invalid setup mode: ${choice:-}" ;;
  esac
}

run_cmd() {
  if [ "$CHECK_ONLY" = "1" ]; then
    log "CHECK_ONLY: would run: $*"
    return 0
  fi
  "$@"
}

run_shell() {
  if [ "$CHECK_ONLY" = "1" ]; then
    log "CHECK_ONLY: would run shell: $*"
    return 0
  fi
  sh -c "$*"
}

sudo_cmd() {
  if [ "$(id -u)" -eq 0 ]; then
    run_cmd "$@"
  elif have_cmd sudo; then
    run_cmd sudo "$@"
  else
    warn "sudo is missing; cannot run privileged command: $*"
    return 1
  fi
}

parse_args() {
  while [ "$#" -gt 0 ]; do
    case "$1" in
      -y|--yes) YES=1 ;;
      --full) YES=1; INSTALL_OPTIONAL=1 ;;
      --minimal) YES=1; INSTALL_OPTIONAL=0 ;;
      --dry-run|--check|--check-only) CHECK_ONLY=1 ;;
      --optional) INSTALL_OPTIONAL=1 ;;
      --copy) INSTALL_MODE=copy ;;
      --symlink) INSTALL_MODE=symlink ;;
      --repo-url) shift; REPO_URL="${1:?missing value for --repo-url}" ;;
      --branch) shift; BRANCH="${1:?missing value for --branch}" ;;
      --repo-dir) shift; REPO_DIR="${1:?missing value for --repo-dir}"; REPO_DIR_EXPLICIT=1 ;;
      --skip-os-packages) SKIP_OS_PACKAGES=1 ;;
      --skip-hermes-install) SKIP_HERMES_INSTALL=1 ;;
      --skip-bootstrap) SKIP_BOOTSTRAP=1 ;;
      -h|--help) usage; exit 0 ;;
      *) die "unknown option: $1" ;;
    esac
    shift
  done
}

refresh_path() {
  export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$HOME/.npm-global/bin:$PATH"
}

detect_repo_from_script() {
  # When executed from an existing checkout, prefer that checkout over REPO_DIR.
  # When piped through curl, BASH_SOURCE is not a real repo path, so this is a no-op.
  local script_dir repo_root
  script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd 2>/dev/null || true)
  if [ -n "$script_dir" ]; then
    repo_root=$(cd -- "$script_dir/.." 2>/dev/null && pwd 2>/dev/null || true)
    if [ "$REPO_DIR_EXPLICIT" != "1" ] && [ -d "$repo_root/.git" ] && [ -d "$repo_root/skills" ]; then
      REPO_DIR="$repo_root"
    fi
  fi
}

install_os_basics() {
  if [ "$SKIP_OS_PACKAGES" = "1" ]; then
    log "skipping OS package installation by request"
    return 0
  fi

  local missing=0
  for cmd in git curl bash python3; do
    if ! have_cmd "$cmd"; then missing=1; fi
  done
  if ! have_cmd npm; then missing=1; fi

  if [ "$missing" = "0" ]; then
    log "base commands present: git curl bash python3 npm"
    return 0
  fi

  if [ "$CHECK_ONLY" = "1" ]; then
    log "CHECK_ONLY: would install missing OS packages with apt-get/brew where supported"
    return 0
  fi

  if have_cmd apt-get; then
    if [ "$YES" != "1" ] && ! confirm "Install missing OS packages with apt-get?"; then
      warn "skipped OS package installation"
      return 0
    fi
    sudo_cmd apt-get update
    sudo_cmd apt-get install -y git curl ca-certificates bash python3 nodejs npm
  elif have_cmd brew; then
    if [ "$YES" != "1" ] && ! confirm "Install missing packages with Homebrew?"; then
      warn "skipped Homebrew package installation"
      return 0
    fi
    run_cmd brew install git curl python node
  else
    warn "no supported OS package manager found (apt-get/brew). Install git curl bash python3 node/npm manually."
  fi
}

configure_node_registry() {
  if ! have_cmd npm; then
    warn "npm missing; Claude/Codex CLI installation may fail"
    return 0
  fi
  if [ "$CHECK_ONLY" = "1" ]; then
    log "CHECK_ONLY: would set npm registry to $NPM_REGISTRY"
    if have_cmd pnpm; then log "CHECK_ONLY: would set pnpm registry to $NPM_REGISTRY"; fi
    return 0
  fi
  npm config set registry "$NPM_REGISTRY" >/dev/null || true
  if have_cmd pnpm; then pnpm config set registry "$NPM_REGISTRY" >/dev/null || true; fi
}

install_hermes_if_missing() {
  refresh_path
  if have_cmd hermes; then
    log "hermes present: $(hermes --version 2>/dev/null | head -1 || true)"
    return 0
  fi
  if [ "$SKIP_HERMES_INSTALL" = "1" ]; then
    warn "hermes missing and --skip-hermes-install was set"
    return 0
  fi
  if [ "$CHECK_ONLY" = "1" ]; then
    log "CHECK_ONLY: would install Hermes Agent using the official installer"
    return 0
  fi
  if [ "$YES" != "1" ] && ! confirm "Install Hermes Agent using the official installer?"; then
    warn "skipped Hermes installation"
    return 0
  fi
  log "installing Hermes Agent with official installer"
  run_shell 'curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash'
  refresh_path
  if have_cmd hermes; then
    log "hermes installed: $(hermes --version 2>/dev/null | head -1 || true)"
  else
    warn "hermes command still missing after installer; open a new shell or add Hermes to PATH"
  fi
}

ensure_repo() {
  if [ -d "$REPO_DIR/.git" ]; then
    log "repository present: $REPO_DIR"
    if git -C "$REPO_DIR" status --short -uall | grep -q .; then
      warn "repository has local changes; skipping pull: $REPO_DIR"
    else
      log "updating repository with git pull --ff-only"
      run_cmd git -C "$REPO_DIR" fetch origin "$BRANCH"
      run_cmd git -C "$REPO_DIR" checkout "$BRANCH"
      run_cmd git -C "$REPO_DIR" pull --ff-only origin "$BRANCH"
    fi
    return 0
  fi

  if [ -e "$REPO_DIR" ]; then
    warn "target exists but is not a git checkout: $REPO_DIR"
    return 0
  fi

  log "cloning Hercules skills repo to $REPO_DIR"
  run_cmd mkdir -p "$(dirname "$REPO_DIR")"
  run_cmd git clone --branch "$BRANCH" "$REPO_URL" "$REPO_DIR"
}

backup_existing_runtime_dir() {
  local runtime="$1"
  if [ ! -e "$runtime" ] && [ ! -L "$runtime" ]; then
    return 0
  fi
  if [ -L "$runtime" ]; then
    if [ "$CHECK_ONLY" = "1" ]; then
      log "CHECK_ONLY: existing symlink would be replaced: $runtime -> $(readlink "$runtime" || true)"
    else
      log "removing existing symlink: $runtime -> $(readlink "$runtime" || true)"
    fi
    run_cmd rm -f "$runtime"
    return 0
  fi
  local backup_dir="$HOME/.hermes/backups/skills/hercules.$(date +%Y%m%d-%H%M%S)"
  warn "existing runtime directory will be moved to backup: $backup_dir"
  run_cmd mkdir -p "$(dirname "$backup_dir")"
  run_cmd mv "$runtime" "$backup_dir"
}

install_skills() {
  local src="$REPO_DIR/skills"
  local runtime_root="${HERMES_HOME:-$HOME/.hermes}/skills"
  local runtime="$runtime_root/hercules"

  if [ "$CHECK_ONLY" != "1" ] && [ ! -d "$src" ]; then
    die "skills directory not found: $src"
  fi

  run_cmd mkdir -p "$runtime_root"
  if [ "$INSTALL_MODE" = "copy" ]; then
    backup_existing_runtime_dir "$runtime"
    log "copying Hercules skills to $runtime"
    run_cmd mkdir -p "$runtime"
    if [ "$CHECK_ONLY" = "1" ]; then
      log "CHECK_ONLY: would copy $src/. to $runtime/"
    else
      cp -a "$src/." "$runtime/"
    fi
  elif [ "$INSTALL_MODE" = "symlink" ]; then
    backup_existing_runtime_dir "$runtime"
    log "linking Hercules skills: $runtime -> $src"
    run_cmd ln -sfn "$src" "$runtime"
  else
    die "unknown install mode: $INSTALL_MODE"
  fi
}

run_repo_validation() {
  if [ "$CHECK_ONLY" = "1" ]; then
    log "CHECK_ONLY: would run repository validation in $REPO_DIR"
    return 0
  fi
  if [ -x "$REPO_DIR/scripts/hercules" ]; then
    (cd "$REPO_DIR" && scripts/hercules validate)
  elif [ -f "$REPO_DIR/scripts/validate-skill-pack.py" ]; then
    (cd "$REPO_DIR" && python3 scripts/validate-skill-pack.py && git diff --check && bash -n skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh)
  else
    warn "validator not found under $REPO_DIR"
  fi
}

run_dependency_bootstrap() {
  if [ "$SKIP_BOOTSTRAP" = "1" ]; then
    log "skipping Hercules dependency bootstrap by request"
    return 0
  fi
  local bootstrap="$REPO_DIR/skills/hercules-agent-capability-preflight/scripts/bootstrap-hercules-workflow.sh"
  if [ ! -f "$bootstrap" ]; then
    if [ "$CHECK_ONLY" = "1" ]; then
      log "CHECK_ONLY: would run Hercules dependency bootstrap at $bootstrap"
      return 0
    fi
    warn "bootstrap script not found: $bootstrap"
    return 0
  fi
  log "running Hercules dependency bootstrap"
  HERCULES_YES="$YES" \
  HERCULES_CHECK_ONLY="$CHECK_ONLY" \
  HERCULES_INSTALL_OPTIONAL="$INSTALL_OPTIONAL" \
  NPM_REGISTRY="$NPM_REGISTRY" \
  bash "$bootstrap"
}

print_next_steps() {
  cat <<EOF

[hercules-install] Done.

Next steps for a fresh machine:
  1. If Hermes has not been configured yet: hermes setup
  2. If Claude Code auth is missing:    claude auth login --console
  3. If Codex auth is missing:          codex login
  4. Start a fresh Hermes session:       hermes --tui
  5. Load Hercules preflight:            /skill hercules-agent-capability-preflight

Useful checks:
  cd "$REPO_DIR"
  scripts/hercules doctor
  scripts/hercules status
  scripts/hercules validate

Repair helpers:
  scripts/hercules doctor --fix        # minimal repair
  scripts/hercules doctor --fix --full # include optional Claude plugins

Installed skill path:
  ${HERMES_HOME:-$HOME/.hermes}/skills/hercules
EOF
}

main() {
  if [ "$#" -eq 0 ]; then
    prompt_setup_mode
  else
    parse_args "$@"
  fi
  detect_repo_from_script
  refresh_path

  log "starting install (check_only=$CHECK_ONLY yes=$YES optional=$INSTALL_OPTIONAL mode=$INSTALL_MODE)"
  log "repo_url=$REPO_URL"
  log "branch=$BRANCH"
  log "repo_dir=$REPO_DIR"

  install_os_basics
  configure_node_registry
  install_hermes_if_missing
  ensure_repo
  install_skills
  run_repo_validation
  run_dependency_bootstrap
  print_next_steps
}

main "$@"
