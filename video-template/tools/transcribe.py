# Word-timestamp Arabic transcription (used to time captions). Setup:
#   python3 -m venv work/venv && work/venv/bin/pip install faster-whisper
#   ffmpeg -i clip.mov -vn -ac 1 -ar 16000 work/audio/c1.wav
#   work/venv/bin/python -I tools/transcribe.py work/audio/c1.wav > work/transcript_c1.json
# NOTE: Palestinian/Levantine dialect is transcribed imperfectly (use model "medium"). ALWAYS proofread: write the final
# caption text by hand, keep only the *timings* from here, and leave a gap rather than guess a word you cannot hear.
import sys, json
from faster_whisper import WhisperModel
m = WhisperModel("medium", compute_type="int8")
segs, _ = m.transcribe(sys.argv[1], language="ar", word_timestamps=True, vad_filter=True)
print(json.dumps([{"s": s.start, "e": s.end, "t": s.text.strip(),
                   "w": [(w.word.strip(), round(w.start, 2), round(w.end, 2)) for w in s.words]} for s in segs], ensure_ascii=False, indent=1))
