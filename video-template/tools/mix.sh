#!/bin/bash
# Voice (trimmed + cleaned + normalised) + music bed ducked under voice + SFX  ->  work/audio/final.wav
# 1) Edit the CLIPS array below: "inputFile:startSec:endSec" in timeline order (must match the page's clip trims).
# 2) python3 -m pip install numpy ; python3 -I reel/audio.py work/audio    (generates music.wav + sfx.wav; edit SFX times in audio.py)
# 3) TOTAL = total video seconds (voice is padded with silence up to it)
set -e
HERE="$(cd "$(dirname "$0")/.." && pwd)"
FF="$HERE/node_modules/ffmpeg-static/ffmpeg"; [ -x "$FF" ] || FF="$(command -v ffmpeg)"
RAW="${RAW:-$HERE/raw}"; A="$HERE/work/audio"; mkdir -p "$A"
TOTAL=86.5
CLIPS=("1.mov:0:17.7" "2.MOV:0:4.7" "3.MOV:0:21.4" "4.mov:0.2:31.1" "5.mov:0:10.2")
INS=(); FC=""; CAT=""; i=0
for c in "${CLIPS[@]}"; do IFS=: read f s e <<< "$c"; INS+=(-i "$RAW/$f"); FC+="[$i:a]atrim=$s:$e,asetpts=PTS-STARTPTS[a$i];"; CAT+="[a$i]"; i=$((i+1)); done
"$FF" -v error -y "${INS[@]}" -filter_complex "${FC}${CAT}concat=n=$i:v=0:a=1,aresample=44100,\
highpass=f=85,afftdn=nr=12:nf=-30,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1:g=3,\
acompressor=threshold=-24dB:ratio=3.2:attack=8:release=140:makeup=6,loudnorm=I=-15:TP=-1.5:LRA=7,apad=whole_dur=$TOTAL,atrim=0:$TOTAL[v]" -map "[v]" -ac 2 "$A/voice.wav"
"$FF" -v error -y -i "$A/voice.wav" -i "$A/music.wav" -i "$A/sfx.wav" -filter_complex "\
[1:a]volume=0.9[m];[m][0:a]sidechaincompress=threshold=0.03:ratio=7:attack=15:release=450:makeup=1[md];\
[2:a]volume=0.75[s];[0:a][md][s]amix=inputs=3:normalize=0:duration=longest,volume=0.74,alimiter=limit=0.9,atrim=0:$TOTAL[o]" \
  -map "[o]" -c:a pcm_s16le "$A/final.wav"
echo "mixed -> $A/final.wav  (target ~ -15 LUFS)"
