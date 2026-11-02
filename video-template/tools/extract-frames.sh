#!/bin/bash
# Extract 30fps JPEG frames from a raw clip (ffmpeg auto-applies iPhone rotation metadata).
# usage: tools/extract-frames.sh <input.mov> <clipName> [startSec=0] [durationSec] [crop=none|screen]
#   crop=screen  -> for iPhone screen recordings (1290x2796): cut the status bar (top 150px) and scale to 960 wide
# Output: work/frames/<clipName>/0001.jpg ...   (frame i = local time (i-1)/30 s)
set -e
HERE="$(cd "$(dirname "$0")/.." && pwd)"
FF="$HERE/node_modules/ffmpeg-static/ffmpeg"; [ -x "$FF" ] || FF="$(command -v ffmpeg)"
IN="$1"; NAME="$2"; SS="${3:-0}"; DUR="$4"; CROP="${5:-none}"
OUT="$HERE/work/frames/$NAME"; mkdir -p "$OUT"
VF="fps=30"; [ "$CROP" = "screen" ] && VF="fps=30,crop=1290:2646:0:150,scale=960:-2"
ARGS=(-v error -y -ss "$SS" -i "$IN"); [ -n "$DUR" ] && ARGS+=(-t "$DUR")
"$FF" "${ARGS[@]}" -vf "$VF" -q:v 3 "$OUT/%04d.jpg"
echo "$NAME: $(ls "$OUT" | wc -l) frames -> $OUT"
