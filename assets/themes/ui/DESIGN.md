# Ui — Style Reference
> brutalist Swiss grid in graphite and chalk. A designer's drafting table where every line is a 1px border, every surface is white, and the only accent is a filled-black button that cuts like a blade through all that negative space.

**Theme:** light

shadcn/ui is a strictly monochromatic design system documentation site: pure white canvas, graphite text, and hairline #e5e5e5 borders doing all the structural work. There is zero brand color — the system IS the absence of color, which is the point. Typography (Geist) carries the identity: weight 600 at 48px with -0.05em tracking gives the hero a tight, almost architectural gravity, while body text at 14-16px stays quiet and utilitarian. Components are compact, grid-driven, and border-first: 10px radii, 1px hairline separators, and an almost complete absence of shadow or elevation. The one filled element on the page is the black primary button — it sits like a period at the end of a sentence, deliberate and unmissable against all the white space around it.

## Tokens — Colors

| Name | Value | Token | Role |
|------|-------|-------|------|
| Graphite | `#0a0a0a` | `--color-graphite` | Dark supporting neutral for text, icons, and strong contrast. Do not promote it to the primary CTA color |
| Pure Black | `#000000` | `--color-pure-black` | Body text, icon fills, link text, and the darkest border variant — the default ink |
| Carbon | `#171717` | `--color-carbon` | Dark surface for inverted cards, dark-mode preview tiles, and badge backgrounds — sits one step above graphite for subtle dark layering |
| Concrete | `#737373` | `--color-concrete` | Secondary body text, muted labels, placeholder content — the workhorse mid-gray for non-primary copy |
| Ash | `#a1a1a1` | `--color-ash` | Disabled state borders, extremely subtle dividers |
| Smoke | `#b9b9b9` | `--color-smoke` | Soft borders on less-emphasized containers |
| Hairline | `#e5e5e5` | `--color-hairline` | The dominant structural color — every card border, input border, table separator, and nav divider is this exact shade. Frequency 1225 makes it the load-bearing wall of the entire system |
| Mist | `#f2f2f2` | `--color-mist` | Subtle surface fill for tags, ghost button hover, and micro-backgrounds — the lightest gray that still registers as not-white |
| Chalk | `#ffffff` | `--color-chalk` | Page canvas, card surfaces, button text on dark fills, input backgrounds — the dominant surface at all levels |

## Tokens — Typography

### Geist — Every text context on the site — body, buttons, icons-as-labels, badges, nav, inputs, cards, headings. Geist is a custom Vercel geometric sans with quiet, slightly squared terminals. Its 1.43 line-height at 14-16px creates a compact utilitarian rhythm; at 48px with weight 600 and -0.05em tracking it becomes the only moment of typographic drama. The tight tracking on larger sizes (-0.05em) is signature — text feels set in concrete, not floating · `--font-geist`
- **Substitute:** Inter, system-ui, -apple-system, sans-serif
- **Weights:** 400, 500, 600
- **Sizes:** 12px, 13px, 14px, 16px, 18px, 48px
- **Line height:** 1.43 (body), 1.20 (headings), 1.50 (UI elements)
- **Letter spacing:** -0.05em at display sizes (48px), -0.025em at body-subhead range, normal at 12-14px UI text
- **OpenType features:** `"cv11", "ss01"`
- **Role:** Every text context on the site — body, buttons, icons-as-labels, badges, nav, inputs, cards, headings. Geist is a custom Vercel geometric sans with quiet, slightly squared terminals. Its 1.43 line-height at 14-16px creates a compact utilitarian rhythm; at 48px with weight 600 and -0.05em tracking it becomes the only moment of typographic drama. The tight tracking on larger sizes (-0.05em) is signature — text feels set in concrete, not floating

### Geist Mono — Monospace input fields, code-adjacent text, and technical micro-copy where character width consistency matters. Detected only in input context at 14px · `--font-geist-mono`
- **Substitute:** ui-monospace, "SF Mono", "Cascadia Code", monospace
- **Weights:** 400
- **Sizes:** 14px
- **Line height:** 1.43
- **Role:** Monospace input fields, code-adjacent text, and technical micro-copy where character width consistency matters. Detected only in input context at 14px

### Type Scale

| Role | Size | Line Height | Letter Spacing | Token |
|------|------|-------------|----------------|-------|
| caption | 12px | 1.5 | — | `--text-caption` |
| body | 14px | 1.43 | — | `--text-body` |
| subheading | 18px | 1.5 | -0.45px | `--text-subheading` |
| display | 48px | 1.1 | -2.4px | `--text-display` |

## Tokens — Spacing & Shapes

**Density:** compact

### Spacing Scale

| Name | Value | Token |
|------|-------|-------|
| 4 | 4px | `--spacing-4` |
| 5 | 5px | `--spacing-5` |
| 6 | 6px | `--spacing-6` |
| 8 | 8px | `--spacing-8` |
| 10 | 10px | `--spacing-10` |
| 12 | 12px | `--spacing-12` |
| 16 | 16px | `--spacing-16` |
| 20 | 20px | `--spacing-20` |
| 24 | 24px | `--spacing-24` |
| 32 | 32px | `--spacing-32` |
| 40 | 40px | `--spacing-40` |
| 80 | 80px | `--spacing-80` |
| 83 | 83px | `--spacing-83` |

### Border Radius

| Element | Value |
|---------|-------|
| nav | 10px |
| cards | 14px |
| pills | 9999px |
| badges | 26px |
| inputs | 10px |
| buttons | 10px |

### Shadows

| Name | Value | Token |
|------|-------|-------|
| subtle | `lab(100 0 0) 0px 0px 0px 2px` | `--shadow-subtle` |
| subtle-2 | `oklab(0.145 -0.00000143796 0.00000340492 / 0.1) 0px 0px 0...` | `--shadow-subtle-2` |

### Layout

- **Page max-width:** 1200px
- **Section gap:** 48px
- **Card padding:** 16px
- **Element gap:** 8px

## Components

### Top Navigation Bar
**Role:** Global site navigation

Horizontal bar on white background, 64px height, items separated by 10px gaps. Logo at far left, nav links (Docs, Components, Blocks, Charts, Directory, Create) in 14px Geist weight 500 #0a0a0a. Search input centered/right, GitHub link with count badge, and a filled black "New" button at far right. No background fill on the nav itself — it relies on the page canvas and a subtle bottom border at #e5e5e5.

### Search Input
**Role:** Documentation search field

White background, 1px solid #e5e5e5 border, 10px border-radius, 10px vertical and 12px horizontal padding. Placeholder text "Search documentation..." in #737373. Focus state shows a 2px ring at #ffffff (inverted outline pattern). Geist weight 400 at 13-14px.

### Pill Badge (Introducing Sora)
**Role:** Feature announcement tag

Rounded pill with ~26px border-radius. #f2f2f2 background, 2px vertical and 10-12px horizontal padding. Geist weight 500 at 12px in #0a0a0a. Often paired with a right-arrow chevron icon.

### Primary Filled Button
**Role:** Primary call-to-action

Black (#0a0a0a) background, white (#ffffff) text, 10px border-radius, 4-8px vertical and 16px horizontal padding. Geist weight 500 at 14px. Used for "New Project" and "New" — the only high-contrast filled element in the system. No shadow. Hover may slightly lighten the background.

### Ghost Text Button
**Role:** Secondary action

No background, no border. Text only in #0a0a0a at 14px Geist weight 500. Used for "View Components" beside the primary CTA. Hover state adds #f2f2f2 background.

### Component Preview Card
**Role:** Showcase tile for a UI component example

White (#ffffff) background, 1px solid #e5e5e5 border, 14px border-radius, 16-20px internal padding. Contains a labeled example of a single component (Payment Method, Team Members, AI Input, Appearance Settings, etc.). Some cards use an extremely subtle 1px shadow at oklab(0.145 0 0 / 0.1) for the barest hint of separation. Section headers inside cards are 16-18px Geist weight 600 in #0a0a0a; helper text is 13-14px in #737373.

### Text Input
**Role:** Form text entry

White background, 1px solid #e5e5e5 border, 10px border-radius, 8-10px vertical and 10-12px horizontal padding. Geist 14px weight 400. Placeholder in #737373. Focus state: 2px outer ring in #ffffff (inverted ring effect) or border darkens to #0a0a0a.

### Toggle / Switch
**Role:** Binary on/off control

Rounded track (~20px height, ~9999px radius) in #e5e5e5 off-state, #0a0a0a on-state. Thumb is white circle. No label inside — label sits adjacent. Pairs with descriptive text in #737373.

### Checkbox with Label
**Role:** Agreement or option selection

Square 16px box, 1px #e5e5e5 border, 4px radius. Checked state fills with #0a0a0a and shows white checkmark. Label text at 14px Geist weight 400 in #0a0a0a sits immediately right.

### Select / Dropdown Trigger
**Role:** Option picker

Same dimensions as text input. Shows current value in #0a0a0a, placeholder in #737373. Right-side chevron icon in #737373. 10px border-radius, 1px #e5e5e5 border.

### Slider
**Role:** Range value input

Horizontal track in #e5e5e5, filled portion in #0a0a0a. Thumb is a small circle. 4px height on track. No border or shadow. Label "Price Range" above in 14px Geist weight 500.

### Tab / Segmented Control
**Role:** Switching between related views

Inline group of text labels (Syncing, Updating, Loading) with small status dot icons. No background container. Active state may have a subtle underline or bold weight. 6px gap between items.

### Radio Group Item
**Role:** Single-selection option

Circular radio with outer ring at #e5e5e5 and inner dot at #0a0a0a when selected. Label text beside it in 14px Geist. Used inside the Compute Environment card.

### Tag / Chip
**Role:** Inline metadata or filter

Rounded shape (~26px radius), #f2f2f2 or white background with #e5e5e5 border, 2-4px vertical and 8-10px horizontal padding. 12-13px Geist weight 500 text. May include a leading icon.

### Dark Surface Card
**Role:** Inverted contrast element

Uses #171717 as background with white or light-gray text. Same 14px radius and 16px padding as light cards. Used sparingly for visual punctuation (dark mode previews, terminal-style blocks, or notification surfaces).

## Do's and Don'ts

### Do
- Use #0a0a0a as the fill for the single primary action button on any screen — never use #171717, #737373, or any lighter gray for a filled CTA
- Use #e5e5e5 for all 1px borders — cards, inputs, table rows, dividers, nav separators. It is the structural color of the system
- Use 10px border-radius for buttons, inputs, and nav items; 14px for cards; ~26px for tags; 9999px only for true pill shapes
- Use Geist at 14px weight 400 with 1.43 line-height for body text, and 48px weight 600 with -0.05em letter-spacing for display headings
- Keep section gaps at 48px and element gaps at 8px — the system is compact, not spacious; never let whitespace exceed the hairline grid
- Use #737373 for all secondary/muted text and #0a0a0a for all primary text; never use a chromatic gray or a tinted neutral
- When showing a filled button next to a secondary action, use the filled black button + ghost text button pattern — never two filled buttons side by side

### Don't
- Do not introduce any chromatic color — no blues, greens, reds, or purples for buttons, links, icons, or accents. The system is strictly achromatic
- Do not use shadows for elevation. Cards separate via 1px #e5e5e5 borders, not box-shadow. The only permitted shadow pattern is the 1px oklab outline ring
- Do not use border-radius values outside the scale: 4px, 10px, 14px, 26px, 9999px. No 6px, 8px, 12px, 16px, or 20px radii
- Do not use a sans-serif other than Geist (or its substitute Inter) — avoid decorative, humanist, or serif typefaces
- Do not use letter-spacing wider than 0 at any size — the system tracks tight (-0.05em at display, -0.025em at subhead) and never goes positive
- Do not place more than one filled black button in the same visual region — the system uses single primary actions surrounded by ghost and surface controls
- Do not use gradients of any kind — fills are always solid; the system has no gradient vocabulary

## Surfaces

| Level | Name | Value | Purpose |
|-------|------|-------|---------|
| 0 | Canvas | `#ffffff` | Page background — the base layer everything sits on |
| 1 | Card | `#ffffff` | Component preview cards share the canvas color, separated only by 1px #e5e5e5 borders |
| 2 | Muted Surface | `#f2f2f2` | Tags, ghost button hovers, pill badges, subtle micro-backgrounds |
| 3 | Inverted Surface | `#171717` | Dark-mode preview tiles, inverted cards, notification surfaces — the single dark surface in an otherwise light system |

## Elevation

The system deliberately avoids box-shadow for elevation. Separation is achieved entirely through 1px hairline borders in #e5e5e5. The only shadow-like effect is a 1px outer ring using oklab(0.145 0 0 / 0.1) on certain cards, which reads as a slightly darker border rather than true elevation. This border-first philosophy keeps the UI flat, architectural, and reminiscent of wireframes — appropriate for a design-system documentation site where components should be readable as structure, not as finished product.

## Imagery

No photography, no illustration, no decorative imagery. The site is pure UI: the components themselves (payment forms, team lists, settings panels, chat inputs) serve as the visual content. Icons are minimal line-art at 16px in #737373 or #0a0a0a, drawn at ~1.5px stroke weight. The visual density comes from the grid of component preview cards, not from imagery — each card is a self-contained micro-screenshot of a real component in its natural state.

## Agent Prompt Guide

**Quick Color Reference**
- text: #0a0a0a (primary), #737373 (secondary/muted)
- background: #ffffff (canvas/card), #f2f2f2 (muted surface), #171717 (inverted)
- border: #e5e5e5 (hairline), #a1a1a1 (disabled), #0a0a0a (emphasis)
- accent: none — the system has no chromatic accent
- primary action: no distinct CTA color

**Example Component Prompts**

No distinct primary action color was observed; use the extracted neutral button treatments instead of inventing a filled CTA color.

2. **Component Preview Card**: White background, 1px solid #e5e5e5 border, 14px border-radius, 16px padding. Card title at 16px Geist weight 600 in #0a0a0a. Helper text at 13px Geist weight 400 in #737373. Content area below with compact 8px gaps between elements.

3. **Form Input**: White background, 1px solid #e5e5e5 border, 10px border-radius, 10px vertical / 12px horizontal padding. Placeholder text in #737373 at 14px Geist weight 400. Value text in #0a0a0a.

4. **Pill Badge**: #f2f2f2 background, 26px border-radius, 4px vertical / 10px horizontal padding. 12px Geist weight 500 in #0a0a0a. Optional leading icon in #737373 at 12px.

5. **Settings Row with Toggle**: Horizontal row, 8px gap between label and control. Label at 14px Geist weight 500 in #0a0a0a, sub-label at 13px Geist weight 400 in #737373. Toggle on the right: 20px height track, 9999px radius, #0a0a0a when on, #e5e5e5 when off, white circular thumb.

## Similar Brands

- **Vercel** — Shares the Geist typeface and the strictly black-and-white aesthetic with 10px radii — the visual DNA is essentially the same
- **Linear** — Same compact density, same hairline-border-first approach, same absence of decorative color in favor of pure structural geometry
- **Radix UI** — Both are unstyled component library sites with minimal chrome — the cards and documentation layout patterns are nearly identical
- **Tailwind CSS** — Documentation sites with the same stark white canvas, no marketing imagery, and component-grid as the primary content pattern
- **Geist UI** — Shares the Geist font and the monochromatic, border-driven component aesthetic at matching scale

## Quick Start

### CSS Custom Properties

```css
:root {
  /* Colors */
  --color-graphite: #0a0a0a;
  --color-pure-black: #000000;
  --color-carbon: #171717;
  --color-concrete: #737373;
  --color-ash: #a1a1a1;
  --color-smoke: #b9b9b9;
  --color-hairline: #e5e5e5;
  --color-mist: #f2f2f2;
  --color-chalk: #ffffff;

  /* Typography — Font Families */
  --font-geist: 'Geist', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-geist-mono: 'Geist Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

  /* Typography — Scale */
  --text-caption: 12px;
  --leading-caption: 1.5;
  --text-body: 14px;
  --leading-body: 1.43;
  --text-subheading: 18px;
  --leading-subheading: 1.5;
  --tracking-subheading: -0.45px;
  --text-display: 48px;
  --leading-display: 1.1;
  --tracking-display: -2.4px;

  /* Typography — Weights */
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;

  /* Spacing */
  --spacing-4: 4px;
  --spacing-5: 5px;
  --spacing-6: 6px;
  --spacing-8: 8px;
  --spacing-10: 10px;
  --spacing-12: 12px;
  --spacing-16: 16px;
  --spacing-20: 20px;
  --spacing-24: 24px;
  --spacing-32: 32px;
  --spacing-40: 40px;
  --spacing-80: 80px;
  --spacing-83: 83px;

  /* Layout */
  --page-max-width: 1200px;
  --section-gap: 48px;
  --card-padding: 16px;
  --element-gap: 8px;

  /* Border Radius */
  --radius-md: 4px;
  --radius-lg: 10px;
  --radius-xl: 14px;
  --radius-3xl: 26px;
  --radius-full: 9996px;
  --radius-full-2: 9999px;
  --radius-full-3: 159981px;
  --radius-full-4: 159984px;

  /* Named Radii */
  --radius-nav: 10px;
  --radius-cards: 14px;
  --radius-pills: 9999px;
  --radius-badges: 26px;
  --radius-inputs: 10px;
  --radius-buttons: 10px;

  /* Shadows */
  --shadow-subtle: lab(100 0 0) 0px 0px 0px 2px;
  --shadow-subtle-2: oklab(0.145 -0.00000143796 0.00000340492 / 0.1) 0px 0px 0px 1px;

  /* Surfaces */
  --surface-canvas: #ffffff;
  --surface-card: #ffffff;
  --surface-muted-surface: #f2f2f2;
  --surface-inverted-surface: #171717;
}
```

### Tailwind v4

```css
@theme {
  /* Colors */
  --color-graphite: #0a0a0a;
  --color-pure-black: #000000;
  --color-carbon: #171717;
  --color-concrete: #737373;
  --color-ash: #a1a1a1;
  --color-smoke: #b9b9b9;
  --color-hairline: #e5e5e5;
  --color-mist: #f2f2f2;
  --color-chalk: #ffffff;

  /* Typography */
  --font-geist: 'Geist', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-geist-mono: 'Geist Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

  /* Typography — Scale */
  --text-caption: 12px;
  --leading-caption: 1.5;
  --text-body: 14px;
  --leading-body: 1.43;
  --text-subheading: 18px;
  --leading-subheading: 1.5;
  --tracking-subheading: -0.45px;
  --text-display: 48px;
  --leading-display: 1.1;
  --tracking-display: -2.4px;

  /* Spacing */
  --spacing-4: 4px;
  --spacing-5: 5px;
  --spacing-6: 6px;
  --spacing-8: 8px;
  --spacing-10: 10px;
  --spacing-12: 12px;
  --spacing-16: 16px;
  --spacing-20: 20px;
  --spacing-24: 24px;
  --spacing-32: 32px;
  --spacing-40: 40px;
  --spacing-80: 80px;
  --spacing-83: 83px;

  /* Border Radius */
  --radius-md: 4px;
  --radius-lg: 10px;
  --radius-xl: 14px;
  --radius-3xl: 26px;
  --radius-full: 9996px;
  --radius-full-2: 9999px;
  --radius-full-3: 159981px;
  --radius-full-4: 159984px;

  /* Shadows */
  --shadow-subtle: lab(100 0 0) 0px 0px 0px 2px;
  --shadow-subtle-2: oklab(0.145 -0.00000143796 0.00000340492 / 0.1) 0px 0px 0px 1px;
}
```
