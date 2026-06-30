# Minimal Mono Theme

Minimal Mono is a black, white, and warm gray color theme. It keeps the RicoUI layout and typography but removes saturated color from the interface.

## Runtime

- Theme id: `minimal-mono`
- Applied with: `<html data-theme="minimal-mono">`
- Stored in: `localStorage.theme_id`
- Dark mode is layered with: `<html class="dark" data-theme="minimal-mono">`

## Light Tokens

| Token | Value | Usage |
| --- | --- | --- |
| `--color-primary` | `#1a1a1a` | Brand color, headings, links, icons |
| `--color-primary-strong` | `#333333` | Hover and emphasis |
| `--color-primary-light` | `#b1b0b0` | Soft accents and disabled states |
| `--color-accent` | `#f5f3f1` | Quiet highlight surfaces |
| `--color-bg-primary` | `#fdfcfc` | Page canvas |
| `--color-bg-secondary` | `#ffffff` | Cards and panels |
| `--color-text-primary` | `#1a1a1a` | Heading color |
| `--color-text-secondary` | `#57534f` | Body text |
| `--color-text-tertiary` | `#777169` | Muted metadata |
| `--color-btn-primary` | `#1a1a1a` | Filled button background |
| `--color-btn-primary-hover` | `#333333` | Filled button hover |
| `--color-btn-primary-text` | `#ffffff` | Filled button text |

## Dark Tokens

| Token | Value | Usage |
| --- | --- | --- |
| `--color-primary` | `#f4f4f2` | Brand color in dark mode |
| `--color-primary-strong` | `#ffffff` | Hover and emphasis |
| `--color-primary-light` | `#d2d2cf` | Soft accents |
| `--color-accent` | `#2a2927` | Quiet highlight surfaces |
| `--color-bg-primary` | `#11110f` | Page canvas |
| `--color-bg-secondary` | `#1a1917` | Cards and panels |
| `--color-text-primary` | `#f4f4f2` | Heading color |
| `--color-text-secondary` | `#d8d5cf` | Body text |
| `--color-text-tertiary` | `#aaa49b` | Muted metadata |
| `--color-btn-primary` | `#f4f4f2` | Filled button background |
| `--color-btn-primary-hover` | `#ffffff` | Filled button hover |
| `--color-btn-primary-text` | `#11110f` | Filled button text |

## Guidance

- Use this theme for editorial, documentation, portfolio, and minimal product sites.
- Avoid adding new saturated accents. The restraint is the point.
- Keep all component geometry unchanged; this theme should feel like a color discipline, not a separate template.
