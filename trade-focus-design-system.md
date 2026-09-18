# Trade Focus Design System — "Greek nautical" typographic manifesto
Implementation spec for the Trade Focus style (trade-focus.com). Hand to any dev agent as-is. Sibling of `keel-design-system.md` (KEEL keeps its own orange system; this is the parent brand).

## 1. Color tokens
```css
:root {
  --bg: #F9FBFE;          /* page ground: near-white, faintly blue */
  --bg-2: #EDF3FA;        /* alternate section ground (quiet rhythm) */
  --ink: #0F1722;         /* primary text, buttons-on-light hover, footer bg */
  --ink-soft: #33404F;    /* body copy */
  --ink-muted: #5F6E7E;   /* secondary text, nav links, labels */
  --ink-faint: #8595A6;   /* captions, scroll cues */
  --accent: #0D5EAF;      /* FLAG BLUE — structure: numbers, dashes, buttons, links */
  --sea: #1FA7EA;         /* AEGEAN — the vibrant second blue, for lines that must stand */
  --gold: #D9A62E;        /* GOLD — the rare third note */
  --keel-orange: #FF4D00; /* product color; appears ONLY on KEEL references */
  --accent-tint: #E8F0FB; /* soft blue wash */
  --accent-on-dark-1: #D6E7FA; /* body copy on flag-blue bg */
  --accent-on-dark-2: #B9D6F5; /* muted labels on flag-blue bg */
  --navy: #0E2740;        /* THE DARK SECTION: deep marine, never plain black */
  --card: #FFFFFF;        /* cards on the ground */
  --line: #D9E2EC;        /* hairlines, section dividers (1px) */
  --line-dark: #23405C;   /* dividers on navy */
  --text-on-dark: #AFC3D6;/* body copy on navy */
}
::selection { background: var(--accent); color: var(--bg); }
```

### Accent discipline (the governing rule)
Three chromatic voices, strictly cast:
- **Flag blue** = structure and action. Section numbers + their 32px dash, buttons, nav hovers, link underlines, the wordmark's full stop.
- **Aegean** = vibrancy. One phrase or line per moment that must stand: an emphasized phrase in a statement, the hardest line in the dark section, the "solution" line.
- **Gold** = value, sparingly (3–4 places per page total): *finance*, the founder's rule, the payoff word ("certainty"). Gold is jewelry — if it appears twice in one viewport, demote one.
- **KEEL orange** never colors Trade Focus UI; it appears only as the product's identity mark (its status dot / tag in listings). The parent is blue; the product is orange; the contrast is intentional.

## 2. Typography
Two families only:
- **Archivo** (400/500/600/700/800/900) — everything.
- **IBM Plex Mono** (400/500) — labels, section numbers, signatures, meta.

```css
@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800;900&family=IBM+Plex+Mono:wght@400;500&display=swap');
```

Scale (the page IS the type — no imagery):
- Opening wordmark: `clamp(88px, 19.5vw, 330px)` / 900 / line-height .86 / letter-spacing −.025em, uppercase, stacked to fill the viewport width; full stop in --accent.
- `.xl` statement: `clamp(34px, 5.4vw, 76px)` / 800 / 1.03 / −.03em / max-width 20ch.
- `.lg` statement: `clamp(24px, 3.4vw, 46px)` / 700 / 1.12 / −.02em / max-width 26ch.
- `.md` body: `clamp(19px, 2.1vw, 28px)` / 400 / 1.5 / --ink-soft / max-width 52ch.
- Mono label: 11–13px, uppercase, letter-spacing .08–.12em, --ink-muted.
- Emphasis inside statements: italic (`.em-i`) for spoken/quoted terms, color classes (`.orange`→accent, `.sea`, `.gold`) for the cast voices. Bold leads in body: 600, --ink.
- Base body: 17px/1.6 Archivo.

## 3. Layout & rhythm
- Container: max-width 1200px, padding 0 32px (20px under 600px).
- Sections separated by 1px --line; padding `clamp(80px, 12vh, 130px) 0`.
- **Background rhythm**: default --bg; alternate key sections on --bg-2; ONE navy inversion (--navy) for the hardest argument; ONE full-accent section (--accent bg) for the close/contact. Max 4 grounds per page.
- Content stacks vertically: `.stack` = flex column, gap `clamp(26px, 4.5vh, 44px)`. One thought per block, read line by line. No columns in the manifesto flow; no cards for argumentation.

## 4. Section anatomy (the signature pattern)
Every section opens with a mono index row:
```
[ 01 in --accent, IBM Plex Mono 13px ] [ 32px × 1px --accent dash ] [ optional mono label in --ink-muted ]
```
gap 12px, margin-bottom `clamp(36px, 6vh, 56px)`. Numbering is sequential and load-bearing.

Special moments:
- **The opening**: 100vh section; giant stacked wordmark; beneath it a 1px --ink rule with a mono strapline row (left: what you do; right: territory), then a tracked-out mono scroll cue ("READ ↓").
- **The dark section (navy)**: the indictment/hardest claim. Statement in --bg, its sharpest line in `.sea`. Signatures in gold.
- **The founder note**: own quiet section — `.lg` weight 600, max-width 34ch, 3px solid --gold left border, padding-left clamp(18px,3vw,32px); mono uppercase signature in --ink-muted below.
- **The equation/payoff**: stacked `.xl` lines, tight gap (`clamp(10px,2vh,20px)`), each line a different cast voice, last line gold.
- **Closing italic**: `.md .em-i` — the personal line that ends the manifesto.

## 5. Components
**Nav** — fixed top, 64px, `rgba(249,251,254,.92)` + `backdrop-filter: blur(8px)`, 1px --line bottom border. Wordmark 800/17px/.14em tracking. Links 14px/500 --ink-muted, hover --accent. Right: language pills + pill CTA. Under 600px: links hidden, everything compacts to one row.

**Buttons** — pill (radius 999px), 600 weight, no borders.
- Primary: --accent bg, --bg text; hover → --ink bg. Padding 14px 30px (nav small: 10px 22px).
- Ghost: transparent, 1.5px --accent border, --accent text; hover inverts.
- On accent-bg sections: --ink bg, --bg text; hover → --bg bg + --accent text.

**Language toggle** — two mono 12px pills (EN/ES); active = --ink bg. Persisted in localStorage; `html[lang]` shows/hides `[lang]` spans.

**List rows (developments pattern)** — no cards: full-width rows with 1px --ink top border (and bottom on the last), `grid-template-columns: 200px 1fr` (stacks under 860px). Left: mono uppercase status tag — dot + words, colored by identity (product color for live products, --ink-muted hollow dot for in-development). Right: h3 800 `clamp(30px,4.2vw,56px)`, a 600-weight tagline, body, and a mono underlined link (`border-bottom: 1px solid --ink`, hover --accent).

**Contact card** — --card bg, 1px --line, radius 16px, padding 28px, max-width 720px, sits on the accent section. Labels mono 11px uppercase --ink-muted; inputs --bg fill, 1px --line, radius 12px, focus border --accent (no ring). Submit = primary pill.

**Footer** — --ink bg, mono 13px, --ink-faint text; brand 700 Archivo with .1em tracking in --bg.

## 6. Motion
- One pattern: `.rise` reveal — opacity 0 / translateY(18–22px) → in view, `.8s cubic-bezier(.2,.7,.2,1)`, staggered `transitionDelay = (i % 6, capped 3) * 0.08s`, IntersectionObserver threshold .12–.15, unobserve after firing.
- Hover transitions color/background only, ~150ms.
- No parallax, no scroll-driven text, no counters. `prefers-reduced-motion`: reveals render instantly, smooth scroll off.

## 7. Voice cues (for layout decisions)
The page is a manifesto: sentences arrive one at a time at display sizes, and the layout never decorates them. When copy names things people "speak" or values, give each its cast color (accent/sea/gold) as italic emphasis — color IS the illustration. Arguments are never carded; only inventory (developments, forms) may use rows/cards. Everything bilingual EN/ES via paired `[lang]` spans; localized, not translated.

## 8. Exclude
Stock imagery, illustration, icons. Card grids for ideas. More than one navy and one accent section per page. Gold anywhere it doesn't mean value. Any second typeface. Shadows — hairlines and grounds do the work.
