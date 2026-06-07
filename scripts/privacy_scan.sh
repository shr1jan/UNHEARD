#!/usr/bin/env bash
# Static privacy gate (defense-in-depth alongside the runtime tests).
# (E5-1 NFR-PRIV-02, E5-4 NFR-PRIV-03)
#
# Fails the build if the raw-audio code paths contain disk-write primitives.
# The runtime guard (services/masking/masking/guards.py) is the primary defense;
# this catches obvious regressions in code review / CI before tests even run.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fail=0

# Directories that handle raw audio / transcripts in-memory only.
SCAN_DIRS=(
  "$ROOT/services/masking/masking"
  "$ROOT/services/moderation/moderation"
)

# Files allowed to mention disk primitives (the guard itself names them to block them).
ALLOWLIST_RE='guards\.py'

scan() {
  local pattern="$1" label="$2"
  for dir in "${SCAN_DIRS[@]}"; do
    [ -d "$dir" ] || continue
    # grep returns 1 when no matches — that's success here.
    if matches=$(grep -rEnI "$pattern" "$dir" 2>/dev/null | grep -Ev "$ALLOWLIST_RE" || true); [ -n "$matches" ]; then
      echo "✗ PRIVACY GATE: $label found on a raw-audio path:"
      echo "$matches" | sed 's/^/    /'
      fail=1
    fi
  done
}

echo "== Privacy scan (raw-audio paths must not write to disk) =="
scan "tempfile" "tempfile usage"
scan "open\s*\([^)]*['\"][^'\"]*[wax]\+" "open(...) in write mode"
scan "\.write\s*\(" "file .write( call"

if [ "$fail" -ne 0 ]; then
  echo ""
  echo "Raw audio and transcripts must stay in memory only (NFR-PRIV-01/02)."
  echo "If a write is genuinely needed off the audio path, move it out of these"
  echo "packages or wrap audio handling in masking.guards.no_disk_writes()."
  exit 1
fi

echo "✓ No disk-write primitives on raw-audio paths."
