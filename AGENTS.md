# AGENTS.md — production agent for Al Ameer Hydraulics content

You turn raw phone footage / app screenshots into **branded Arabic reels, stories and posts**. Read `brand/BRAND.md` first.

## Non-negotiables
1. **Arabic, RTL, Palestinian/Levantine dialect** for on-screen copy unless told otherwise. Never retype the logo — use `brand/logos/logo-circle.png`.
2. **Colours only from `brand/tokens.json`** (black `#0B0B0C`, gold `#F4B300` / `#FFD25E`). No new accent colours (red is only for "no/✕" stamps, green only for WhatsApp).
3. **Never invent claims** (prices, "مجاني", discounts, phone numbers, availability). Use only what the speaker said or what the app screenshot shows. If a word in the audio is unintelligible, leave the caption gap and flag it to the user.
4. **Captions must match the speech.** Transcribe with `video-template/tools/transcribe.py`, then proofread by hand; keep timings, fix text.
5. **Reels:** 1080×1920, 30 fps, ≤ 90 s, keep key content inside y∈[220, 1540] (Instagram UI covers top/bottom), loudness ≈ −15 LUFS, true peak ≤ −1 dB.
6. Don't commit raw footage, rendered frames, `node_modules/`, `work/` (already in `.gitignore`). Final videos: hand them to the user, don't commit unless asked.
7. Don't touch `main`/app code. This branch is assets + tooling only.

## Workflow — reel
1. Probe clips (`ffprobe`), watch contact sheets, transcribe (word timestamps). Decide a **cut list** in speech order (cut only dead air at clip ends).
2. `tools/extract-frames.sh <clip> <name> <start> <dur> [screen]` for each clip → `work/frames/<name>/`.
3. Copy `video-template/reel/` to a new folder, edit **only the data blocks** in `index.html` (see `docs/REEL-GUIDE.md`): `T`, `CAP`, `OFF`, `kw`/stamps, `STEPS`, `CAM`, `HL`, `TAPS`, `ZK`, scene-swap times.
4. `tools/preview.sh <page> "t1,t2,…" sheet.jpg` — check text overlap, safe zones, highlight positions; iterate until clean.
5. `tools/render-parallel.sh <page> work/out <seconds> 3` → frames; edit `tools/mix.sh` CLIPS + `reel/audio.py` SFX times → `tools/mix.sh`; `tools/encode.sh work/out work/audio/final.wav out.mp4`.
6. Verify: duration, `ebur128` loudness, a few frames (first frame must not be black — it becomes the thumbnail), captions vs. audio.

## Workflow — image
Copy a file from `templates/`, change text/screenshot, `tools/html2png.mjs … <w> <h>`, look at the PNG, iterate. See `docs/IMAGE-GUIDE.md`.

## When something is missing
Ask the user for: logo variant (transparent wordmark doesn't exist yet), product/machine photos (source = Firebase), exact claims/prices, phone/WhatsApp numbers, the speaker's name/title.
