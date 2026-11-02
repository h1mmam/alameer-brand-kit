# Making posts, stories & thumbnails

Static images are **HTML → PNG** with headless Chrome: full CSS control, exact brand components, repeatable.

```bash
cd video-template && npm install            # once (only needed for video; images need just Chrome + Node)
node tools/html2png.mjs ../templates/post-1080x1350.html  ../out/post.png  1080 1350
node tools/html2png.mjs ../templates/story-1080x1920.html ../out/story.png 1080 1920
node tools/html2png.mjs page.html out.jpg 1080 1350 2      # 4th arg scale: 2 = retina export
```
Formats: post 1080×1350 · square 1080×1080 · story/reel cover 1080×1920 (safe y 220→1540) · OG/link 1200×630.

## Recipe
1. `cp templates/story-1080x1920.html templates/my-new.html` (keep it in `templates/` so `../brand/...` paths resolve).
2. Change headline/sub/stamps, swap the screenshot path (`../assets/app-screens/*.jpg`), keep `<link rel="stylesheet" href="../brand/brand.css">`.
3. Render → open the PNG → fix overlaps → repeat. Check at phone size (zoom out) that the headline reads in 1 second.

## Components in `brand/brand.css`
`.canvas` `.bg-glow` `.bg-chev` `.logo-chip` `.badge` `.card` `.stamp` `.chip` `.cta` `.sb-app` `.sb-gp` `.phone` `.cap` — see the file; each is 3–6 lines and designed for a 1080-wide canvas.

## App screenshots in a phone frame
`assets/app-screens/*.jpg` are 1290×2646 (iPhone status bar already cropped). `.phone .screen` is 640×1313 — the **same aspect**, so
`<div class="phone"><div class="screen"><img src="…"><div class="island"></div></div></div>` needs no cropping. Scale the whole `.phone` with CSS `transform: scale(.8)`.
To zoom on a UI element, put the `<img>` in a `overflow:hidden` box and scale/translate it (screen-fraction positions: button row y≈0.609 → x 0.18 / 0.50 / 0.81; WhatsApp button on details page y≈0.551).
`machine-details-bobcat.jpg` was captured mid-slide (dim photo) — prefer `machine-details-bobcat-b.jpg`.

## Do / don't
- Do keep ≤ 8 words per headline, one gold word for emphasis, one CTA.
- Don't add prices/discounts/phone numbers not given by the user; don't crop the logo circle; don't use white backgrounds.
- Machine photos: the only clean one here is `assets/photos/machine-bobcat-e19.jpg`. For others ask the user to export from the app / Firebase.

## Carousel / multi-slide
Duplicate a template per slide, render each to `out/slide-01.png …`; keep headline position identical across slides and swap only the screenshot + text.
