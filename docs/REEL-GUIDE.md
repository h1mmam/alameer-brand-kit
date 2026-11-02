# Reel engine — how the 86 s reel was built and how to make the next one

Reference output: `examples/reel-preview-540p.mp4` (+ `examples/reel-keyframes/`). Source of truth: `video-template/reel/index.html`.

## Architecture (why it looks the way it does)
- **One HTML page = the whole video.** `window.seek(t)` computes *every* element's state from the time `t` (pure function, no CSS animations, no accumulated state) and returns a Promise.
- `tools/render.mjs` opens the page in headless Chrome (CDP), calls `seek(t)` for every frame at 30 fps and saves JPEGs. → perfectly deterministic, any frame renderable alone.
- Raw clips are pre-extracted to JPEG sequences (`tools/extract-frames.sh`) and shown via `<img>`; `setFrame(img, clip, localSeconds)` picks frame `round(t*30)+1` and `await img.decode()`s it. (HTML `<video>` seeking is not frame-accurate — don't use it.)
- Audio is built separately (`tools/mix.sh` + `reel/audio.py`), then `tools/encode.sh` muxes frames + audio into MP4.
- Speed: ~0.45 s/frame/process → 86 s ≈ 2600 frames ≈ 3 min with 3 parallel processes (`tools/render-parallel.sh`).

## The data blocks you edit (everything else is engine)
| Block in `index.html` | Meaning |
|---|---|
| `T`, `END`, `SW1`, `SW2`, `C4OFF` | global timeline: where each clip starts, total length, instants where scene A→B swaps (hidden under a wipe), offset of a clip trimmed from a non-zero start |
| `CAP` | captions per clip: `[start,end,'text']` in **clip-local** seconds; `OFF` maps clip-local → global. Words are highlighted proportionally to length inside the interval |
| `ZK` | talking-head punch-in zoom keys `[t0,t1,scale0,scale1]` (hard "jump-cut" zooms every sentence → rhythm) |
| `kw[]`, `st1..3` | talking-head overlays: glass keyword cards and red ✕ stamps, each with `anim(el,t,t0,t1,kind)` calls in `seek` |
| `STEPS` | phone-scene header titles `[t0,t1,badge,title,subtitle]` |
| `CAM` | virtual camera keys `[t, scale, fx, fy, ty]`; `(fx,fy)` = focus point in *screen fractions* (0–1), `ty` shifts the frame vertically. Interpolated with ease-in-out |
| `HL` | spotlight rectangles `[t0,t1,fx,fy,fw,fh]` (screen fractions) |
| `TAPS` | tap ripples `[t,fx,fy]` — place them **0.1–0.3 s before** the app visibly reacts |
| chips / chat card / stamps2 / badges | overlays during the phone scene (`anim(...)` lines in the phone-scene branch) |
| end card | `#end` markup + the `inEnd` branch (logo elastic pop, ring, text rise, CTA pulse) |

### Geometry
Canvas 1080×1920. Phone box `left:208 top:220 664×1337`; screen = 640×1313 at canvas (220,232). Recordings are cropped (`crop=1290:2646:0:150`, status bar removed) and scaled to 960 px wide, so a point on the original iPhone frame maps to screen fraction `fy=(srcY−150)/2646`, `fx=srcX/1290`.
Measured positions (home screen): button row `fy≈0.609` — «اعرض آليتك» `fx .18`, «طلب المساعدة» `.50`, «جميع المعدات» `.81`; details page WhatsApp button `fy≈0.551`.
Camera: `translate(540 − s·cx, 888+ty − s·cy) scale(s)` with `(cx,cy)` = focus in canvas px. Highlights live *inside* the screen so they follow camera and 3D tilt automatically.

### Helpers
`anim(el,t,t0,t1,kind,{inD,outD,x,y,rot})` kinds: `right|left|up|pop|slam|fade` (enter, hold, exit). `wipe(t,tSwap,dur)` slash transition — scene content must flip at `tSwap` (it is fully covered then). `E.*` easings (`out3,out5,inOut,back,elastic`). `P(t,a,b)` clamped progress.

## Production recipe (what was actually done)
1. **Probe**: iPhone clips 1,2 = 1080p H.264 with rotation metadata (ffmpeg auto-rotates), clips 3–5 = HEVC screen recordings 1290×2796.
2. **Transcribe** each clip (`tools/transcribe.py`, faster-whisper *medium*, word timestamps). Levantine dialect → proofread by hand; leave unintelligible words uncaptioned and tell the user.
3. **Cut list** in speech order, trimming only dead air at clip ends (speech is continuous, don't cut mid-sentence). Reference: `c1 0–17.7 | c2 0–4.7 | c3 0–21.4 | c4 0.2–31.1 | c5 0–10.2` → 84.9 s + 1.6 s outro tail.
4. **Find UI event times** in screen recordings with scene detection (`select='gt(scene,0.12)'` at 15 fps) → exact instants of taps/transitions to place `TAPS`, `HL`, `CAM`.
5. Edit data blocks, `tools/preview.sh` contact sheets at key instants (wipes, stamps, zoomed highlights, end card), fix overlaps (cards must not cover the face: keep y 230–440; captions sit at y≈1300–1490).
6. Audio: voice chain `highpass 85 → afftdn → EQ (−2 dB@250, +3 dB@3.2k) → acompressor 3.2:1 → loudnorm −15 LUFS`; music = synthesised Am–F–C–G pad+arp+soft kick (`audio.py`, 88 bpm) **sidechain-ducked** under voice; SFX (whoosh at wipes, pops at cards, slam at stamps, click at taps, message ping, boom+shimmer at the logo reveal) timed to the same instants. Final `×0.74` + limiter 0.9 ⇒ ≈ −15.1 LUFS, −0.9 dBTP.
7. Render, encode (`crf 18`, ~55 MB / 86 s), verify duration, loudness (`ffmpeg -af ebur128=peak=true`), first frame (must show the speaker, not black), captions vs. audio.

## Reference timeline (global seconds)
| t | scene |
|---|---|
| 0–17.7 | owner talking head, punch-in zooms, badge «ميزة جديدة», cards «اعرض آليتك للبيع» / «تصفّح الآليات», stamps «بدون وسطاء / بدون عمولات / من البائع للزبون» |
| 17.7–22.4 | "stay with us" clip, card «شرح الميزة خطوة بخطوة» |
| 22.4 | slash wipe → phone scene |
| 22.4–43.8 | how to use «اعرض آليتك»: highlight + tap + WhatsApp chat mock (photo, specs ✓, «تم! بنعرضها») |
| 43.8–74.7 | «طلب المساعدة» → «جميع المعدات» → list → details → WhatsApp button → stamps |
| 74.7–80.1 | download: App Store + Google Play badges, «الرابط بالوصف» |
| 80.1 | slash wipe → end card (logo pop, «شركة الأمير…», CTA) |
| 86.5 | end |

## Pitfalls we hit
- `/tmp` scratch can be cleaned by the OS mid-project → keep `work/` inside the repo folder (it is git-ignored).
- Caption word gap needs ≥ 32 px (outline shadows eat the space). Outline is a `text-shadow` ring (reliable for connected Arabic glyphs; `-webkit-text-stroke` makes spikes).
- First frame black = bad thumbnail → intro wipe starts already ¾ revealed (`wipeFrom(t,.8,pSwap+.3)`).
- Overlays that appear with a hard `display:none` toggle need their `hide` class reset on every `seek` (the page does this at the top of `seek`) or backwards seeking breaks.
- Don't claim what the audio doesn't say (e.g. an unclear «مجانية» was left out of the captions).
- Instagram bottom UI hides y>1540, top y<220: no essential text there (the phone body may overlap).

## Adapting for a new reel
New topic, same style: keep scene structure (hook talking head → wipe → phone demo with spotlights → store badges → end card), replace `CAP`/`STEPS`/`kw`/`HL`/`TAPS`, re-time `CAM`, change `audio.py` SFX instants to the new instants, update `mix.sh` CLIPS + `TOTAL`. For a screen-recording-only reel drop the talking-head branch (set `SW1=0`).
