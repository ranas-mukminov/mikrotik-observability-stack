#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="${1:-${PROJECT_ROOT}/config/mikrotik-devices.example.yml}"
export PYTHONPATH="${PROJECT_ROOT}/cli:${PYTHONPATH:-}"

python -m mosctl.cli validate-config --config "${CONFIG}"
