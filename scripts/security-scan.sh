#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

STATUS=0
if command -v pip-audit >/dev/null 2>&1; then
  pip-audit || STATUS=$?
else
  echo "[security] pip-audit not installed, skipping" >&2
fi

if command -v trivy >/dev/null 2>&1; then
  trivy config compose || STATUS=$?
  trivy fs --exit-code 1 --severity CRITICAL,HIGH compose docker || STATUS=$?
else
  echo "[security] trivy not installed, skipping" >&2
fi

exit ${STATUS}
