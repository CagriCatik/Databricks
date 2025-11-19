#!/usr/bin/env bash
# Robust MATLAB Proxy init for Azure Databricks
# - Driver-only
# - Forces port 3000 (matches Dockerfile)
# - Starts with a clean environment to ignore image defaults
# - Optional HTTPS proxy and NLM
# - Writes URL and logs to /databricks/driver/matlab-proxy
# - Warms up MATLAB once to reduce post-login delay
# - Never fails the cluster

set -uo pipefail

# Run only on driver
if [[ "${DB_IS_DRIVER:-false}" != "true" && "${DB_IS_DRIVER:-false}" != "TRUE" ]]; then
  exit 0
fi

LOG_DIR="/databricks/driver/matlab-proxy"
LOG_FILE="${LOG_DIR}/matlab-proxy.out"
PID_FILE="${LOG_DIR}/matlab-proxy.pid"
URL_FILE="${LOG_DIR}/matlab-url.txt"
mkdir -p "${LOG_DIR}"
: > "${LOG_FILE}"

echo "$(date -Is) INFO: init start" | tee -a "${LOG_FILE}"

# Optional corporate proxy for outbound HTTPS (uncomment if needed)
# export HTTPS_PROXY=http://proxy.company.com:3128
# export HTTP_PROXY=http://proxy.company.com:3128
# export NO_PROXY=localhost,127.0.0.1,::1,.azuredatabricks.net

# Preferred licensing: set NLM if available (bypasses MathWorks Online Licensing)
# export MLM_LICENSE_FILE="27000@licenseserver.company.com"

# Fixed config to align with Databricks driver-proxy
PORT="3000"
BASE="/matlab"

# Path and binary
PATH="/databricks/python3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
MP_BIN="$(command -v matlab-proxy-app || true)"
if [[ -z "${MP_BIN}" ]]; then
  echo "$(date -Is) ERROR: matlab-proxy-app not found on PATH=${PATH}" | tee -a "${LOG_FILE}"
  exit 0
fi

# Kill stale proxy (wrong env/port)
if pgrep -f "matlab-proxy-app" >/dev/null 2>&1; then
  echo "$(date -Is) INFO: killing stale matlab-proxy-app" | tee -a "${LOG_FILE}"
  pkill -f "matlab-proxy-app" || true
  sleep 2
fi

# Start proxy in verbose mode with a clean environment so image defaults cannot override
echo "$(date -Is) INFO: starting matlab-proxy-app on 0.0.0.0:${PORT}${BASE}" | tee -a "${LOG_FILE}"
env -i \
  PATH="${PATH}" \
  HOME="/databricks/driver" \
  TMPDIR="/tmp" \
  XDG_RUNTIME_DIR="/tmp" \
  MWI_APP_PORT="${PORT}" \
  MWI_BASE_URL="${BASE}" \
  MWI_ENABLE_TOKEN_AUTH="False" \
  MWI_USE_COOKIE_CACHE="True" \
  MWI_HOST="0.0.0.0" \
  MW_CONTEXT_TAGS="MATLAB_PROXY:DATABRICKS:V1" \
  ${MLM_LICENSE_FILE:+MLM_LICENSE_FILE="${MLM_LICENSE_FILE}"} \
  nohup "${MP_BIN}" --verbose >>"${LOG_FILE}" 2>&1 &

echo $! > "${PID_FILE}"

# Health check loop for proxy HTTP
HC_URL="http://127.0.0.1:${PORT}${BASE}"
for i in $(seq 1 90); do
  if command -v curl >/dev/null 2>&1 && curl -s -I "${HC_URL}" | grep -qE "^HTTP/.* (200|301|302)"; then
    echo "$(date -Is) INFO: proxy healthy at ${HC_URL}" | tee -a "${LOG_FILE}"
    URL="https://${DATABRICKS_INSTANCE:-adb-unknown}/driver-proxy/o/${DATABRICKS_ORG_ID:-unknown}/${DB_CLUSTER_ID:-unknown}/${PORT}${BASE}"
    printf "%s\n" "${URL}" | tee "${URL_FILE}" >/dev/null
    echo "$(date -Is) INFO: URL -> ${URL_FILE}" | tee -a "${LOG_FILE}"
    break
  fi
  # log listening ports for debugging
  if comm
