#!/bin/bash
# Render the whole timeline with N parallel Chrome processes (default 3).
# usage: tools/render-parallel.sh <page.html> <outDir> <totalSeconds> [N=3]
set -e
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PAGE="$1"; OUT="$2"; TOTAL="$3"; N="${4:-3}"
FR="$HERE/work/frames"; mkdir -p "$OUT"
TOTALF=$(python3 -c "print(round($TOTAL*30))")
PER=$(( (TOTALF + N) / N ))
for ((k=0;k<N;k++)); do
  a=$((k*PER)); b=$(( (k+1)*PER - 1 )); [ $b -gt $TOTALF ] && b=$TOTALF
  [ $a -gt $TOTALF ] && continue
  node "$HERE/tools/render.mjs" "$PAGE" "$FR" "$OUT" 30 "$(python3 -c "print($a/30)")" "$(python3 -c "print($b/30)")" > "$HERE/work/render_$k.log" 2>&1 &
done
wait; echo "frames: $(ls "$OUT" | wc -l)"
