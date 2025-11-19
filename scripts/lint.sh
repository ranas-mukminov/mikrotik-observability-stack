#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

run_if_exists() {
  if command -v "$1" >/dev/null 2>&1; then
    "$@"
  else
    echo "[lint] $1 not found, skipping" >&2
  fi
}

run_if_exists ruff check cli tests
run_if_exists black --check cli tests

if command -v yamllint >/dev/null 2>&1; then
  yamllint -c <(cat <<'YAML'
---
extends: default
rules:
  line-length:
    level: warning
YAML
) .
else
  echo "[lint] yamllint not found, skipping" >&2
fi

run_if_exists shellcheck scripts/*.sh
