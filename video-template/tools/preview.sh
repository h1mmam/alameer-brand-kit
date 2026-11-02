#!/bin/bash
# Render a few instants and tile them into one contact sheet (fast visual QA before a full render).
# usage: tools/preview.sh <page.html> "t1,t2,t3,..." <out.jpg> [cols] [tileWidth]
set -e
HERE="$(cd "$(dirname "$0")/.." && pwd)"
FF="$HERE/node_modules/ffmpeg-static/ffmpeg"; [ -x "$FF" ] || FF="$(command -v ffmpeg)"
PAGE="$1"; TIMES="$2"; OUT="$3"; T="$HERE/work/preview"
rm -rf "$T"; mkdir -p "$T"
TIMES="$TIMES" node "$HERE/tools/render.mjs" "$PAGE" "$HERE/work/frames" "$T" >/dev/null
i=0; IFS=, read -ra A <<< "$TIMES"
for t in "${A[@]}"; do i=$((i+1)); cp "$T/f_$(printf "%.2f" "$t").jpg" "$T/s_$(printf %03d $i).jpg"; done
N=${#A[@]}; C=${4:-$N}; ROWS=$(( (N+C-1)/C ))
"$FF" -v error -y -i "$T/s_%03d.jpg" -vf "scale=${5:-360}:-1,tile=${C}x${ROWS}:padding=4" -frames:v 1 "$OUT"
echo "sheet: $OUT"
