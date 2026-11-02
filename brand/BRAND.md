# Brand guide — Al Ameer Hydraulics (الأمير للمعدات وقطع الغيار)

**What it is:** a shop + mobile app (iOS / Android) in Palestine selling hydraulic parts and heavy-equipment spare parts, and — new — a
marketplace section where owners **list their own machines for sale** ("اعرض آليتك") with **no middlemen and no commissions**
(direct contact over WhatsApp).

## Logo
- `brand/logos/logo-circle.png` (819×819, RGBA): circular badge — dark machinery photo, **gold excavator-arm/roof chevron mark** + white wide-italic **ALAMEER** + "FOR EQUIPMENT AND SPARE PARTS".
- Use it **as a circle** with a thin gold ring (`.logo-chip` in `brand.css`) on dark backgrounds. Minimum 90 px on a 1080-wide canvas.
- Don't recolour, stretch, retype the wordmark, or put it on light/busy backgrounds without the dark circle. There is **no transparent wordmark file** yet — ask the user if you need one.
- Other: `app-icon-1024.jpg` (store icon), `favicon-819.png`, `social-preview-1200x630.png`, `splash-dark|light.png`.

## Colour (see `tokens.json`)
| Token | Hex | Use |
|---|---|---|
| bg | `#0B0B0C` | all backgrounds (app uses `#0E0E0E`) |
| panel / panel2 | `#1B1B1B` / `#242424` | cards |
| **gold** | `#F4B300` | brand accent, buttons, highlights, active caption word (`#FFC21A`) |
| gold light | `#FFD25E` | subtitles, gradients (`gold-grad`) |
| app gold | `#E0A11B` / muted `#D6B56D` | only when mimicking in-app UI |
| white | `#FFFFFF` | headlines |
| muted | `#A9A9A9` | secondary text |
| danger `#FF3B3B` | only the ✕ "بدون وسطاء / بدون عمولات" stamps |
| whatsapp `#25D366` | only WhatsApp UI/cards |

Look = **black + gold, glass cards, soft gold glows, thin gold rims**. Never white backgrounds, never gradients other than gold/black.

## Typography
- Arabic UI font in the reference work: **SF Arabic Rounded** (macOS system font — *not redistributable*, so it is **not** in this repo). Weights 600–900; headlines 900.
- Portable stand-ins (Google Fonts, same feel): **Cairo**, **Tajawal**, **Noto Sans Arabic**. `brand.css` already lists the fallback stack.
- Sizes on a 1080 canvas: headline 96–112, captions 84–88, card title 58, sub 32–42, chips 44.
- Arabic text must be **RTL**, real Arabic punctuation (« » ؟ ،), numbers can stay Latin digits (prices ₪).

## Motifs
- **Chevron lines** (the logo's roof/arm shape) in gold, 15–50 % opacity, drifting slowly behind content.
- **Slash wipe** — 20° skewed black panel with gold edge stripes sweeping across, logo flashing in the middle. Used for scene changes.
- **Spotlight highlight** — dim everything, gold rounded rectangle around the UI element being explained + white tap ripple.
- **Phone frame** — dark bezel with gold hairline, floating, slight 3D tilt.
- **Glass keyword card** — gold icon tile + bold title + gold subtitle, slides in from the right.
- **Red ✕ stamps** that "slam" in (scale 2.4→1 with small rotation).

## Voice & copy (Palestinian / Levantine, friendly, direct)
Short, imperative, no fluff. Examples taken from the owner's own words: «اعرض آليتك للبيع»، «بدون وسطاء وبدون أي عمولات»، «تواصل مباشر مع صاحب الآلية»،
«طلب المساعدة»، «جميع المعدات»، «حمّل التطبيق من الرابط بالوصف»، «ثقتكم فينا ودافعنا دايماً نقدم لكم الأفضل».
- Address the viewer as «انت/إنك»; formal-lite Levantine ("بتقدر", "حاب", "هسا").
- Emojis sparingly as icon tiles (🚜 🔍 📲 💬 ✅ 🤝 🔥 ⬇), never in captions.
- **Never state prices, discounts, "free", stock, or contact numbers unless supplied by the user.**

## App facts you can safely reference (visible in `assets/app-screens`)
Home: machines carousel (JCB 3CX, Bobcat mini, E17 …), buttons **«اعرض آليتك» / «طلب المساعدة» / «جميع المعدات»**, news ticker, «تصفح حسب النوع» (قطع غيار، شحمة، كوشوك، فلاتر، زيوت…), TOHREN British brand section, «الخصومات» section, cart, favourites, notifications, bottom tabs (الرئيسية، المنتجات، الجديد، الخصومات). «جميع الآليات» list → machine details (photos, model, status "متاح للبيع", price in ₪, **«تواصل عبر واتساب»** button).
Store badges: `brand/badges/`. The app is downloaded via the link in the bio/description ("الرابط بالوصف").

## Reels spec
1080×1920 · 30 fps · H.264 + AAC · ≤ 90 s · safe area y 220→1540 · burned-in word-highlight captions at y≈1300–1490 · music ducked under voice · ≈ −15 LUFS.
