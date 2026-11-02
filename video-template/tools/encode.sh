#!/bin/bash
# usage: tools/encode.sh <framesOutDir> <audio.wav> <out.mp4>   (frames named f_00000.jpg ..., 30fps)
set -e
HERE="$(cd "$(dirname "$0")/.." && pwd)"
FF="$HERE/node_modules/ffmpeg-static/ffmpeg"; [ -x "$FF" ] || FF="$(command -v ffmpeg)"
"$FF" -v error -y -framerate 30 -i "$1/f_%05d.jpg" -i "$2" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -profile:v high \
  -movflags +faststart -c:a aac -b:a 256k -shortest -r 30 "$3"
echo "wrote $3"
