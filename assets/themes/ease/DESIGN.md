# Ease Health — Style Reference
> Sunlit clinic on white linen. A muted, light-first healthcare surface where one deep forest green does the work of accent, action, and trust, framed by sage washes, dusty-blue panels, and whisper-weight serif headlines.

**Theme:** light

Ease Health uses a clinical-calm language: warm sage and dusty blue surfaces on a near-white canvas, with a single deep forest green carrying every action, icon, and heading accent. The page breathes — generous whitespace, no shadows, thin gray hairlines, and pill-shaped tags that feel like medical labels rather than UI chrome. Typography pairs a delicate serif (Faire Octave) for headline moments with a quiet grotesque (Suisseintl) for everything operational, both set in weight 300 with tight negative tracking so type whispers rather than shouts. Color is rationed: most surfaces are achromatic or barely tinted, and the dark green appears only where the user should act, look, or trust. Components feel light, flat, and confident — the system reads as a calm, premium clinic, not a noisy SaaS dashboard.

## Tokens — Colors

| Name | Value | Token | Role |
|------|-------|-------|------|
| Forest Ink | `#0f3e17` | `--color-forest-ink` | Primary action buttons, heading text, brand icons, footer, active states — the only saturated color in the system; deep enough to read as serious clinical authority against the pale surfaces |
| Sage Wash | `#b1dbb8` | `--color-sage-wash` | Green wash for highlight backgrounds, decorative bands, and soft emphasis behind content. Do not promote it to the primary CTA color |
| Mist Blue | `#b6ced5` | `--color-mist-blue` | Hero panel background, secondary surface tint, pill badge background — the cool counterpoint to sage, used for product/showcase bands |
| Mint Veil | `#cfe7d3` | `--color-mint-veil` | Soft card surface tint, subtle highlight wash |
| Linen | `#e1f4df` | `--color-linen` | Lightest card surface tint, section highlight band |
| Linen White | `#fffefc` | `--color-linen-white` | Page canvas, card surfaces, button text — warm off-white, never pure |
| Hairline Gray | `#e5e7eb` | `--color-hairline-gray` | Borders, dividers, link underlines, nav strokes — the single structural neutral |
| Charcoal | `#222222` | `--color-charcoal` | Navigation link text — softer than pure black, less clinical |
| Graphite | `#333333` | `--color-graphite` | Secondary image borders, muted link color |
| True Black | `#000000` | `--color-true-black` | Primary body and heading text, decorative SVG fills |

## Tokens — Typography

### Suisseintl — Suisseintl — detected in extracted data but not described by AI · `--font-suisseintl`
- **Weights:** 300, 400
- **Sizes:** 12px, 14px, 18px, 23px, 28px, 56px
- **Line height:** 1, 1.3, 1.5
- **Letter spacing:** -0.03
- **Role:** Suisseintl — detected in extracted data but not described by AI

### Faire Octave — Display and section headings only. The serif appears sparingly — two sizes, one weight — to mark narrative moments (hero headline, compliance headline, about headline). Light-weight serif against sans-serif body creates a magazine/editorial cadence; the thin strokes make 74px feel humane rather than corporate. · `--font-faire-octave`
- **Substitute:** Fraunces, Cormorant Garamond, or Playfair Display at weight 300
- **Weights:** 300
- **Sizes:** 40px, 74px
- **Line height:** 1.05–1.35
- **Letter spacing:** -0.0300em, -0.0100em
- **Role:** Display and section headings only. The serif appears sparingly — two sizes, one weight — to mark narrative moments (hero headline, compliance headline, about headline). Light-weight serif against sans-serif body creates a magazine/editorial cadence; the thin strokes make 74px feel humane rather than corporate.

### Suisse Int'l — Body, UI, nav, buttons, badges, and the 56px hero headline. Weight 300 is the default for larger sizes (hero, subheadings) — the anti-convention choice of a light grotesque for a 56px headline makes the page feel airy and unhurried. Weight 400 handles everything 18px and below. The consistent -0.03em tracking across all sizes tightens the grotesque into a refined, considered voice. · `--font-suisse-intl`
- **Substitute:** Inter, Söhne, or Neue Haas Grotesk
- **Weights:** 300, 400
- **Sizes:** 
- **Line height:** 1.00–1.50
- **Letter spacing:** -0.42px at 14px, -0.84px at 28px, -1.68px at 56px
- **OpenType features:** `No special features detected`
- **Role:** Body, UI, nav, buttons, badges, and the 56px hero headline. Weight 300 is the default for larger sizes (hero, subheadings) — the anti-convention choice of a light grotesque for a 56px headline makes the page feel airy and unhurried. Weight 400 handles everything 18px and below. The consistent -0.03em tracking across all sizes tightens the grotesque into a refined, considered voice.

### Type Scale

| Role | Size | Line Height | Letter Spacing | Token |
|------|------|-------------|----------------|-------|
| caption | 12px | 1.5 | -0.36px | `--text-caption` |
| body-sm | 14px | 1.5 | -0.42px | `--text-body-sm` |
| body | 18px | 1.3 | -0.54px | `--text-body` |
| subheading | 23px | 1.3 | -0.69px | `--text-subheading` |
| heading-sm | 28px | 1.3 | -0.84px | `--text-heading-sm` |
| heading | 40px | 1.35 | -0.4px | `--text-heading` |
| heading-lg | 56px | 1 | -1.68px | `--text-heading-lg` |
| display | 74px | 1.05 | -2.22px | `--text-display` |

## Tokens — Spacing & Shapes

**Density:** comfortable

### Spacing Scale

| Name | Value | Token |
|------|-------|-------|
| 4 | 4px | `--spacing-4` |
| 7 | 7px | `--spacing-7` |
| 9 | 9px | `--spacing-9` |
| 11 | 11px | `--spacing-11` |
| 14 | 14px | `--spacing-14` |
| 18 | 18px | `--spacing-18` |
| 21 | 21px | `--spacing-21` |
| 28 | 28px | `--spacing-28` |
| 35 | 35px | `--spacing-35` |
| 42 | 42px | `--spacing-42` |
| 49 | 49px | `--spacing-49` |
| 56 | 56px | `--spacing-56` |
| 70 | 70px | `--spacing-70` |
| 76 | 76px | `--spacing-76` |
| 99 | 99px | `--spacing-99` |
| 156 | 156px | `--spacing-156` |

### Border Radius

| Element | Value |
|---------|-------|
| nav | 7px |
| cards | 14px |
| badges | 999px |
| buttons | 14px |

### Layout

- **Page max-width:** 1200px
- **Section gap:** 80px
- **Card padding:** 21px
- **Element gap:** 21px

## Components

### Primary CTA Button
**Role:** The single high-contrast action on any page — hero, header, conversion points

Filled Forest Ink (#0f3e17) background, Linen White (#fffefc) text at 14px Suisse Int'l weight 400, 14px border-radius, 21px horizontal padding × 14px vertical padding. Includes a right-arrow icon (→) inset in a slightly lighter green outlined square. The dark green-on-warm-white contrast (14.6:1) is the system’s loudest moment by design.

### Header Navigation
**Role:** Top-level site navigation

Linen White background, logo on the left (dark green wordmark), nav links centered or right-aligned in Charcoal (#222222) at 14px Suisse Int'l 400 with 7px border-radius on link containers. 11px horizontal padding on nav items. Book-a-Demo CTA in the top-right using the Primary CTA Button pattern. No background fill, no shadow — sits directly on the canvas.

### Pill Badge / Tag
**Role:** Category labels above section headings (e.g. 'Broad clinical support', 'Standards and reporting')

Mist Blue (#b6ced5) background, Charcoal or black text at 12–14px Suisse Int'l 400, 999px border-radius (full pill), 7–14px vertical padding × 14px horizontal padding. The pill shape echoes medical labeling and stays visually quiet against the white canvas.

### Check Icon Badge
**Role:** Compliance/feature list markers

Forest Ink (#0f3e17) square 32–40px, 7px border-radius, containing a white checkmark. The dark green square is the only spot where the brand color becomes a small visual anchor inside a bulleted list — it earns attention without text.

### Hero Left Panel (Sage)
**Role:** Headline + subtext + CTA in the hero

Sage Wash (#b1dbb8) background filling a full-height left column. Display heading in Faire Octave weight 300 at 74px, Forest Ink (#0f3e17) text, -2.22px tracking. Subtext at 18px Suisse Int'l 400, Charcoal (#222222). The Primary CTA Button sits below with 42px top margin.

### Hero Right Panel (Product Showcase)
**Role:** Product UI cards on a colored band

Mist Blue (#b6ced5) background, full-height right column. Hosts three white product cards (CRM, EHR, RCM) arranged horizontally with 14px gap. Each card is Linen White with 14px border-radius and 21px padding. Small caption labels (CRM/EHR/RCM) sit in white pill badges below each card.

### Product Card
**Role:** Compact product UI mockup (form, profile, chart)

Linen White (#fffefc) background, 14px border-radius, 21px padding, no border, no shadow. Content includes a small avatar, name heading, status text, and a mini Forest Ink button (e.g. 'Submit Note'). The card reads as a screenshot of the product, not a marketing tile.

### Section Heading Block
**Role:** Title + optional tag introducing each content section

Pill Badge stacked above a Faire Octave heading at 40px weight 300 in Forest Ink. 14px vertical gap between badge and heading. Centered or left-aligned depending on section — the system uses left-align for content sections and center for the stats block.

### Two-Column Feature Grid
**Role:** Compliance feature lists, 2×3 grids

Two equal columns with 56px column gap, 28px row gap. Each item pairs a Check Icon Badge with a 14px Suisse Int'l 400 description. No card containers — items sit directly on the canvas, separated by whitespace.

### Stats Block
**Role:** Large quantitative proof points

Two stats side by side. Number in Suisse Int'l weight 300 at 56px, Forest Ink, tight tracking (-1.68px). Label below in 12px Suisse Int'l 400, Charcoal. No dividers, no backgrounds — the scale contrast between the 56px number and 12px label does the work.

### Investor Logo Strip
**Role:** Social proof band — 'Backed by leading investors'

Centered 14px caption 'Backed by leading investors' above a single row of monochrome (black or Charcoal) investor logos at consistent height, evenly spaced with ~35px horizontal padding per logo. No background fill, no border — logos sit on the canvas with generous vertical breathing room (49px row gap).

### Vertical Category List
**Role:** Side-rail navigation of care categories (OBOT, OTP, Eating Disorder, etc.)

Stacked text labels in Suisse Int'l at ~23–28px weight 300, rendered in a very light gray (near Hairline Gray) as a decorative/atmospheric element. Letterspaced wide, no bullets. Reads as ambient typography rather than functional links.

## Do's and Don'ts

### Do
- Use Forest Ink (#0f3e17) as the only saturated color — apply it to the primary action button, headings, checkmark icons, and the logo. Never introduce a second brand color.
- Set headings 40px and above in Faire Octave weight 300 with tight tracking (-0.01em to -0.03em). Body and UI stay in Suisse Int'l.
- Use 14px border-radius for cards and buttons, 999px for badges and tags, 7px for nav items. Do not mix intermediate values like 8px or 12px.
- Build section rhythm with generous whitespace: 80px between sections, 21px between elements, 21px inside cards. The flatness depends on breathing room.
- Communicate elevation through surface tint shifts (Linen White → Mint Veil → Sage Wash → Mist Blue), never through drop shadows.
- Pair every section heading with a Mist Blue pill badge above it — the badge is the system's recurring label device.
- Use 7px vertical × 14px horizontal padding on pill badges to keep them visually compact, not chunky.

### Don't
- Do not add drop shadows to cards, buttons, or sections — the system is intentionally flat and the absence is the design.
- Do not use pure white (#ffffff) — the canvas is Linen White (#fffefc), a warm off-white. Pure white feels cold and clinical in the wrong way.
- Do not use Sage Wash (#b1dbb8) or Mist Blue (#b6ced5) as button backgrounds — those are surface tints, not action colors. Actions are always Forest Ink.
- Do not set body text above 18px in Suisse Int'l weight 400 — weight 300 is reserved for sizes ≥28px to preserve the light/airy voice.
- Do not introduce new border-radius values. The system uses exactly 7px, 14px, and 999px — adding 8px or 12px breaks the geometric consistency.
- Do not stack multiple saturated colors in the same view. One Forest Ink moment per region; let surfaces and whitespace do the structuring.
- Do not use bold (600+) or semibold (500) weights — the system speaks in 300 and 400 only. Heavier weights would break the quiet, premium register.

## Surfaces

| Level | Name | Value | Purpose |
|-------|------|-------|---------|
| 0 | Linen White | `#fffefc` | Page canvas — warm off-white base |
| 1 | Mint Veil | `#cfe7d3` | Tinted content card, subtle highlight band |
| 2 | Linen Green | `#e1f4df` | Lightest card surface tint |
| 3 | Sage Wash | `#b1dbb8` | Accent spotlight surface — hero left panel, product spotlight cards |
| 4 | Mist Blue | `#b6ced5` | Hero right panel, product showcase background, pill badges |

## Elevation

No drop shadows anywhere. Elevation is communicated through surface tint shifts (white → mint → sage → mist blue) and thin #e5e7eb hairline borders. This flatness is the design — it reads as clinical cleanliness, not as a missing feature.

## Imagery

Pure UI-first visual language — no photography, no illustration, no product hero shots. Imagery is limited to monochrome (black or Charcoal) investor logos in a single row and white product UI mockup cards rendered inside the colored hero panel. The product cards themselves act as the 'imagery' — they show actual UI screens (a form completion card, a patient profile with submit button, a revenue chart) rather than stylized illustrations. Icons are minimal and appear only as functional checkmarks inside Forest Ink squares. The system treats whitespace and surface color as the primary visual content.

## Agent Prompt Guide

## Quick Color Reference
- Canvas/surface: #fffefc (Linen White)
- Primary text: #000000
- Border/divider: #e5e7eb (Hairline Gray)
- Brand accent: #0f3e17 (Forest Ink) — headings, icons, checkmark badges
- Surface tints: #b1dbb8 (Sage Wash), #b6ced5 (Mist Blue), #cfe7d3 (Mint Veil), #e1f4df (Linen Green)
- primary action: #0f3e17 (filled action)

## Example Component Prompts

1. Create a Primary Action Button: #0f3e17 background, #fffefc text, 9999px radius, compact pill padding. Use this filled treatment for the main CTA.

2. **Section Header with Pill Tag**: Stack a Mist Blue (#b6ced5) pill badge above a heading. Badge: 'Broad clinical support' in 12px Suisse Int'l 400, #0f3e17 text, 999px border-radius, 7px vertical × 14px horizontal padding. Heading below: 'Ease is built from the ground up for behavioral health practices, with AI at the core.' in Faire Octave weight 300, 40px, #0f3e17, letter-spacing -0.4px, line-height 1.35. 14px gap between badge and heading.

3. **Compliance Feature Grid (2×3)**: Build a two-column grid with 56px column gap and 28px row gap. Each item pairs a 32px Forest Ink (#0f3e17) square (7px radius) with a white checkmark, beside a 14px Suisse Int'l 400 description in #000000. No card containers — items sit on the Linen White (#fffefc) canvas.

4. **Stats Block**: Two stats side by side, centered. Stat 1: '$2.5B+' in 56px Suisse Int'l weight 300, #0f3e17, letter-spacing -1.68px, line-height 1.0, with 'claims processed' label in 12px Suisse Int'l 400 #222222 below. Stat 2: '11M+' with 'payor claims submitted' label. 56px horizontal gap between stats.

5. **Pill Badge Above Heading**: A Mist Blue (#b6ced5) pill at 7px vertical × 14px horizontal padding, 999px border-radius, 12px Suisse Int'l 400 text in #0f3e17. The badge sits 14px above a Faire Octave weight 300 40px heading in #0f3e17. This tag-plus-heading pair is the system's signature section opener.

## Surface Strategy

The system communicates hierarchy through color temperature and saturation, not through shadow or border weight. The progression runs: warm off-white canvas (Linen White #fffefc) → near-white green wash (Linen Green #e1f4df) → mid sage (Mint Veil #cfe7d3) → saturated sage (Sage Wash #b1dbb8) → cool counterpoint (Mist Blue #b6ced5). Each step up adds visual weight without adding a border or shadow. Forest Ink (#0f3e17) sits outside this scale as the only 'dark' surface, reserved for primary actions and small icon anchors. When building new screens, choose the lowest surface tint that still creates enough contrast for the content to read, and never combine two heavily tinted surfaces in the same region.

## Similar Brands

- **Headspace Health** — Same soft green-and-white clinical palette, same flat surfaces with no shadows, same pill-shaped category tags above section headings
- **Spring Health** — Same whisper-weight serif headlines paired with a clean grotesque body, same light-first healthcare aesthetic with a single deep accent color
- **Calm Health** — Same generous whitespace and section-by-section breathing room, same rationed use of one saturated brand color against pale surfaces
- **Tia** — Same editorial-magazine cadence: large light-weight serif headings, sans-serif body, warm off-white canvas, no drop shadows
- **Quartet Health** — Same behavioral-health SaaS positioning with muted sage surfaces, pill badges, and a dark forest-green as the sole action color

## Quick Start

### CSS Custom Properties

```css
:root {
  /* Colors */
  --color-forest-ink: #0f3e17;
  --color-sage-wash: #b1dbb8;
  --color-mist-blue: #b6ced5;
  --color-mint-veil: #cfe7d3;
  --color-linen: #e1f4df;
  --color-linen-white: #fffefc;
  --color-hairline-gray: #e5e7eb;
  --color-charcoal: #222222;
  --color-graphite: #333333;
  --color-true-black: #000000;

  /* Typography — Font Families */
  --font-suisseintl: 'Suisseintl', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-faire-octave: 'Faire Octave', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-suisse-intl: 'Suisse Int'l', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

  /* Typography — Scale */
  --text-caption: 12px;
  --leading-caption: 1.5;
  --tracking-caption: -0.36px;
  --text-body-sm: 14px;
  --leading-body-sm: 1.5;
  --tracking-body-sm: -0.42px;
  --text-body: 18px;
  --leading-body: 1.3;
  --tracking-body: -0.54px;
  --text-subheading: 23px;
  --leading-subheading: 1.3;
  --tracking-subheading: -0.69px;
  --text-heading-sm: 28px;
  --leading-heading-sm: 1.3;
  --tracking-heading-sm: -0.84px;
  --text-heading: 40px;
  --leading-heading: 1.35;
  --tracking-heading: -0.4px;
  --text-heading-lg: 56px;
  --leading-heading-lg: 1;
  --tracking-heading-lg: -1.68px;
  --text-display: 74px;
  --leading-display: 1.05;
  --tracking-display: -2.22px;

  /* Typography — Weights */
  --font-weight-light: 300;
  --font-weight-regular: 400;

  /* Spacing */
  --spacing-4: 4px;
  --spacing-7: 7px;
  --spacing-9: 9px;
  --spacing-11: 11px;
  --spacing-14: 14px;
  --spacing-18: 18px;
  --spacing-21: 21px;
  --spacing-28: 28px;
  --spacing-35: 35px;
  --spacing-42: 42px;
  --spacing-49: 49px;
  --spacing-56: 56px;
  --spacing-70: 70px;
  --spacing-76: 76px;
  --spacing-99: 99px;
  --spacing-156: 156px;

  /* Layout */
  --page-max-width: 1200px;
  --section-gap: 80px;
  --card-padding: 21px;
  --element-gap: 21px;

  /* Border Radius */
  --radius-lg: 7.04px;
  --radius-xl: 14.08px;
  --radius-full: 999px;

  /* Named Radii */
  --radius-nav: 7px;
  --radius-cards: 14px;
  --radius-badges: 999px;
  --radius-buttons: 14px;

  /* Surfaces */
  --surface-linen-white: #fffefc;
  --surface-mint-veil: #cfe7d3;
  --surface-linen-green: #e1f4df;
  --surface-sage-wash: #b1dbb8;
  --surface-mist-blue: #b6ced5;
}
```

### Tailwind v4

```css
@theme {
  /* Colors */
  --color-forest-ink: #0f3e17;
  --color-sage-wash: #b1dbb8;
  --color-mist-blue: #b6ced5;
  --color-mint-veil: #cfe7d3;
  --color-linen: #e1f4df;
  --color-linen-white: #fffefc;
  --color-hairline-gray: #e5e7eb;
  --color-charcoal: #222222;
  --color-graphite: #333333;
  --color-true-black: #000000;

  /* Typography */
  --font-suisseintl: 'Suisseintl', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-faire-octave: 'Faire Octave', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-suisse-intl: 'Suisse Int'l', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

  /* Typography — Scale */
  --text-caption: 12px;
  --leading-caption: 1.5;
  --tracking-caption: -0.36px;
  --text-body-sm: 14px;
  --leading-body-sm: 1.5;
  --tracking-body-sm: -0.42px;
  --text-body: 18px;
  --leading-body: 1.3;
  --tracking-body: -0.54px;
  --text-subheading: 23px;
  --leading-subheading: 1.3;
  --tracking-subheading: -0.69px;
  --text-heading-sm: 28px;
  --leading-heading-sm: 1.3;
  --tracking-heading-sm: -0.84px;
  --text-heading: 40px;
  --leading-heading: 1.35;
  --tracking-heading: -0.4px;
  --text-heading-lg: 56px;
  --leading-heading-lg: 1;
  --tracking-heading-lg: -1.68px;
  --text-display: 74px;
  --leading-display: 1.05;
  --tracking-display: -2.22px;

  /* Spacing */
  --spacing-4: 4px;
  --spacing-7: 7px;
  --spacing-9: 9px;
  --spacing-11: 11px;
  --spacing-14: 14px;
  --spacing-18: 18px;
  --spacing-21: 21px;
  --spacing-28: 28px;
  --spacing-35: 35px;
  --spacing-42: 42px;
  --spacing-49: 49px;
  --spacing-56: 56px;
  --spacing-70: 70px;
  --spacing-76: 76px;
  --spacing-99: 99px;
  --spacing-156: 156px;

  /* Border Radius */
  --radius-lg: 7.04px;
  --radius-xl: 14.08px;
  --radius-full: 999px;
}
```
