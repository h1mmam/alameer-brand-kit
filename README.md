# Al Ameer Hydraulics — Brand & Video Kit  (الأمير للمعدات وقطع الغيار)

Everything another agent/designer needs to **make branded reels, stories and posts** for the *Al Ameer Hydraulics* app and shop:
logos, store badges, app screenshots, colours, components, a working **animated-reel engine**, and written guides.

> This is an **orphan branch** (`brand-kit`) — it contains **no app source code**. Don't merge it into `main`.

```
git clone --branch brand-kit --single-branch https://github.com/h1mmam/alameer-hydraulics.git alameer-kit
```

## Start here
| You want to… | Read |
|---|---|
| Understand the brand (colours, tone, logo rules) | [`brand/BRAND.md`](brand/BRAND.md) |
| Act as the production agent (rules + workflow) | [`AGENTS.md`](AGENTS.md) |
| Make a **reel / video** | [`docs/REEL-GUIDE.md`](docs/REEL-GUIDE.md) |
| Make a **post / story / thumbnail** | [`docs/IMAGE-GUIDE.md`](docs/IMAGE-GUIDE.md) |
| Find a file | [`assets/manifest.json`](assets/manifest.json) |
| See the look | [`examples/`](examples) (reel preview 540p, key frames, template renders) |

## Layout
```
brand/         logos/ badges/ social/ backgrounds/  +  brand.css (components)  tokens.json  BRAND.md
assets/        app-screens/ (clean 1290x2646 screenshots)  app-screens-legacy/  photos/
templates/     post-1080x1350.html  story-1080x1920.html   (HTML -> PNG)
video-template/
   reel/            index.html = the finished 86 s reel (timeline, captions, camera, overlays)  +  audio.py (music+SFX)
   story-promo/     older 56 s app-story video (voice-over by TTS)
   tools/           render.mjs  render-parallel.sh  preview.sh  extract-frames.sh  mix.sh  encode.sh  html2png.mjs  transcribe.py
docs/          REEL-GUIDE.md  IMAGE-GUIDE.md
examples/      reference outputs
```

## Requirements
macOS or Linux · Node 20+ · Google Chrome (or set `CHROME=`) · Python 3 + `numpy` (audio) ·
`cd video-template && npm install` (installs a private `ffmpeg`; nothing global).

## Quick test (30 s)
```bash
cd video-template && npm install
node tools/html2png.mjs ../templates/story-1080x1920.html ../out/story.png 1080 1920     # static image
TIMES=80.5,82,84 node tools/render.mjs reel/index.html work/frames work/t                 # end-card frames of the reel
```

## Not in this repo (on purpose)
Raw footage (the owner's talking-head and screen recordings), the final 55 MB reel, and Apple's *SF Arabic Rounded* font file
(not redistributable — see fonts in `brand/BRAND.md`). Real product/machine photos live in the app's Firebase data, not here.
