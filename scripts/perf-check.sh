#!/usr/bin/env bash
set -euo pipefail
PROFILE="compose/docker-compose.minimal.yml"
START=$(date +%s)

for bin in docker curl jq bc; do
  if ! command -v "${bin}" >/dev/null 2>&1; then
    echo "${bin} is required for perf-check" >&2
    exit 1
  fi
done

docker compose -f "${PROFILE}" up -d --remove-orphans
cleanup() {
  docker compose -f "${PROFILE}" down -v >/dev/null 2>&1 || true
}
trap cleanup EXIT

wait_for() {
  local url=$1
  local timeout=${2:-60}
  local start_seconds=$(date +%s)
  while true; do
    if curl -fsS "$url" >/dev/null 2>&1; then
      return 0
    fi
    if (( $(date +%s) - start_seconds > timeout )); then
      echo "Timeout waiting for $url" >&2
      return 1
    fi
    sleep 2
  done
}

wait_for "http://localhost:${PROMETHEUS_PORT:-9090}/-/ready" 90
wait_for "http://localhost:${GRAFANA_PORT:-3000}/api/health" 90

TARGETS=$(curl -fsS "http://localhost:${PROMETHEUS_PORT:-9090}/api/v1/targets" | jq '.data.activeTargets | length')
if [[ -z "$TARGETS" || "$TARGETS" -eq 0 ]]; then
  echo "Prometheus has no active targets" >&2
  exit 1
fi

QUERY_TIME=$(curl -w '%{time_total}' -o /dev/null -s "http://localhost:${PROMETHEUS_PORT:-9090}/api/v1/query?query=up")
if (( $(echo "$QUERY_TIME > 1.5" | bc -l) )); then
  echo "Prometheus query exceeded 1.5s (${QUERY_TIME}s)" >&2
  exit 1
fi

END=$(date +%s)
echo "Perf check passed in $((END-START))s with $TARGETS targets" >&2
