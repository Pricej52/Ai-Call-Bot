#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
API_DIR="$ROOT_DIR/apps/api"
WEB_DIR="$ROOT_DIR/apps/admin-web"
LEGACY_REQ="$ROOT_DIR/requirements.txt"

pass_count=0
warn_count=0
fail_count=0

pass() { echo "✅ $1"; pass_count=$((pass_count + 1)); }
warn() { echo "⚠️  $1"; warn_count=$((warn_count + 1)); }
fail() { echo "❌ $1"; fail_count=$((fail_count + 1)); }

run_check() {
  local label="$1"
  local cmd="$2"
  if bash -lc "$cmd"; then
    pass "$label"
  else
    fail "$label"
  fi
}

echo "== AI Call Bot operational readiness check =="

echo "-- Tooling --"
run_check "Python is available" "python --version"
run_check "Node.js is available" "node --version"

if command -v docker >/dev/null 2>&1; then
  pass "Docker CLI is available"
  run_check "docker compose file is valid" "cd '$ROOT_DIR' && docker compose config >/dev/null"
else
  warn "Docker CLI is not installed; docker verification skipped"
fi

echo "-- Backend (root) --"
if [ -f "$LEGACY_REQ" ]; then
  if python -m pip install -r "$LEGACY_REQ"; then
    pass "Installed root Python dependencies"
    run_check "Root backend tests" "cd '$ROOT_DIR' && pytest -q"
  else
    warn "Could not install root Python dependencies (network or package index restriction)"
  fi
else
  warn "No root requirements.txt found"
fi

echo "-- API service (apps/api) --"
if [ -f "$API_DIR/requirements.txt" ]; then
  if python -m pip install -r "$API_DIR/requirements.txt"; then
    pass "Installed apps/api Python dependencies"
    run_check "API imports successfully" "cd '$API_DIR' && python -c 'import app.main'"
  else
    warn "Could not install apps/api dependencies (network or package index restriction)"
  fi
else
  warn "No apps/api/requirements.txt found"
fi

echo "-- Admin web --"
if [ -f "$WEB_DIR/package.json" ]; then
  if cd "$WEB_DIR" && npm install; then
    pass "Installed admin-web dependencies"
    run_check "Admin web lint" "cd '$WEB_DIR' && npm run lint -- --no-cache"
    run_check "Admin web build" "cd '$WEB_DIR' && npm run build"
  else
    warn "Could not install admin-web dependencies (network or registry restriction)"
  fi
else
  warn "No apps/admin-web/package.json found"
fi

echo "\nSummary: ${pass_count} passed, ${warn_count} warnings, ${fail_count} failed"

if [ "$fail_count" -gt 0 ]; then
  exit 1
fi
