#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="${1:-${PROJECT_ROOT}/config/mikrotik-devices.example.yml}"
export PYTHONPATH="${PROJECT_ROOT}/cli:${PYTHONPATH:-}"

PYTHON_BIN="$(command -v python || command -v python3 || true)"
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "python interpreter not found" >&2
  exit 127
fi

"${PYTHON_BIN}" -m mosctl.cli validate-config --config "${CONFIG}"
