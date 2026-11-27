#!/usr/bin/env bash
# vault-log.sh — append exact, timestamped change records to a vault's Activity Log.
#
# Usage:
#   vault-log.sh snapshot <vault-dir> <relpath>
#       Save the current content of <relpath> BEFORE you change, rename, or delete it.
#       Skip this for a brand-new file (nothing exists to save).
#
#   vault-log.sh log <vault-dir> <action> <relpath> "<summary>" [<new-relpath>]
#       Run AFTER the change. Writes one entry at the end of 05-Meta/Activity Log.md.
#       <action>: created | updated | superseded | renamed | deleted | external
#       <new-relpath>: only for "renamed" (the new path).
#       "external": a change made outside the skill; no snapshot, so no diff is recorded.
#
# <relpath> is relative to the vault folder, for example "02-Decisions/Decision - Queue.md".
# The timestamp comes from the system clock. Never type a timestamp by hand.

set -euo pipefail

cmd="${1:-}"; vault="${2:-}"; shift 2 || true
[ -d "$vault" ] || { echo "vault-log: vault folder not found: $vault" >&2; exit 1; }
vault="${vault%/}"

snapdir="${TMPDIR:-/tmp}/vault-keeper-snapshots"
key() { printf '%s' "$vault/$1" | (md5sum 2>/dev/null || md5) | cut -d' ' -f1; }

case "$cmd" in
snapshot)
  rel="${1:?relpath required}"
  mkdir -p "$snapdir"
  if [ -f "$vault/$rel" ]; then cp "$vault/$rel" "$snapdir/$(key "$rel")"; else : > "$snapdir/$(key "$rel").absent"; fi
  echo "snapshot saved: $rel"
  ;;

log)
  action="${1:?action required}"; rel="${2:?relpath required}"; summary="${3:?summary required}"; newrel="${4:-}"
  meta="$vault/05-Meta"; logfile="$meta/Activity Log.md"
  project="$(basename "$vault")"
  mkdir -p "$meta"
  ts="$(date '+%Y-%m-%d %H:%M:%S %z')"

  if [ ! -f "$logfile" ]; then
    {
      echo "---"
      echo "title: Activity Log"
      echo "created: $(date '+%Y-%m-%d')"
      echo "tags: [$project, meta, log]"
      echo "---"
      echo
      echo "# Activity Log"
      echo
      echo "Full history of changes to this vault. The skill only adds entries at the end."
      echo "It never edits or removes an old entry. Times come from the system clock."
    } > "$logfile"
  fi

  after_rel="${newrel:-$rel}"
  before="/dev/null"
  s="$snapdir/$(key "$rel")"
  [ -f "$s" ] && before="$s"
  after="/dev/null"
  [ -f "$vault/$after_rel" ] && after="$vault/$after_rel"

  difftext=""
  if [ "$action" != "external" ]; then
    difftext="$(diff -u --label "a/$rel" --label "b/$after_rel" "$before" "$after" || true)"
  fi

  added=0; removed=0
  if [ -n "$difftext" ]; then
    # Skip the two header lines (--- and +++) so content lines that start with "--" or "++" count.
    added="$(printf '%s\n' "$difftext" | awk 'NR > 2 && /^\+/ { n++ } END { print n + 0 }')"
    removed="$(printf '%s\n' "$difftext" | awk 'NR > 2 && /^-/ { n++ } END { print n + 0 }')"
  fi

  # Fence must be longer than any backtick run inside the diff.
  maxrun="$(printf '%s' "$difftext" | { grep -o '`\+' || true; } | awk '{ if (length($0) > m) m = length($0) } END { print m + 0 }')"
  flen=$(( maxrun + 1 )); [ "$flen" -lt 3 ] && flen=3
  fence="$(printf '`%.0s' $(seq 1 "$flen"))"

  {
    echo
    echo "## $ts — $action — \`$rel\`"
    echo
    echo "- **Time:** $ts"
    echo "- **Action:** $action"
    echo "- **File:** \`$rel\`"
    if [ -n "$newrel" ]; then echo "- **New file name:** \`$newrel\`"; fi
    echo "- **Summary:** $summary"
    if [ "$action" = "external" ]; then
      echo "- **Change:** made outside the skill. No exact diff is available."
    elif [ -n "$difftext" ]; then
      echo "- **Change:** +$added lines, −$removed lines"
      echo
      echo "<details>"
      echo "<summary>Exact diff</summary>"
      echo
      echo "${fence}diff"
      printf '%s\n' "$difftext"
      echo "$fence"
      echo
      echo "</details>"
    else
      echo "- **Change:** none in file content (path change only)"
    fi
  } >> "$logfile"

  rm -f "$s" "$snapdir/$(key "$rel").absent"
  echo "logged: $ts $action $rel"
  ;;

*)
  echo "usage: vault-log.sh snapshot|log <vault-dir> ..." >&2
  exit 1
  ;;
esac
