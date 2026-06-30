# Manager Theme and DESIGN.md Handling

Use build-time theme selection for the generated bookmark navigation site. The page shows exactly one selected theme and does not include a runtime theme switcher.

## Built-in Themes

Built-in theme assets live in `assets/themes/`. Present all five options when asking the user to choose a built-in theme; do not infer the available set from examples alone.

- `ease`: default. Paper-toned bookmark directory with ink text, mineral blue accents, and quiet index-like surfaces.
- `kami`: Kami-aligned warm canvas, ivory paper, ink-blue accent, serif-led hierarchy, and whisper-light rings.
- `minimal-mono`: dark black-white-warm-gray navigation with no saturated accent colors.
- `retro-blue`: warm paper navigation with editorial blue headings, soft blue accents, and a restrained gold (`--gold`) secondary highlight.
- `ui`: monochrome shadcn-like Swiss navigation, border-first and minimal.

Each theme has:

- `DESIGN.md`: source design reference.
- `theme.json`: normalized navigation-site tokens. Use the optional `cssVars` map to emit extra semantic custom properties (e.g. retro-blue's `--gold`) alongside the standard tokens.
- `theme.css`: pre-generated CSS used directly for built-in themes when present.

## CLI

```bash
python scripts/rico_bookmarks_manager.py themes
python scripts/rico_bookmarks_manager.py manager --data rico-bookmarks/data/bookmarks.json --theme kami --output rico-bookmarks/site
python scripts/rico_bookmarks_manager.py manager --data rico-bookmarks/data/bookmarks.json --theme ease --output rico-bookmarks/site
python scripts/rico_bookmarks_manager.py manager --data rico-bookmarks/data/bookmarks.json --theme minimal-mono --output rico-bookmarks/site
python scripts/rico_bookmarks_manager.py manager --data rico-bookmarks/data/bookmarks.json --theme retro-blue --output rico-bookmarks/site
python scripts/rico_bookmarks_manager.py manager --data rico-bookmarks/data/bookmarks.json --theme ui --output rico-bookmarks/site
```

## Custom DESIGN.md

`--design path/to/DESIGN.md` remains supported for custom design files. It overrides `--theme` and is parsed into the same semantic CSS variable surface. This compatibility path is intentionally lightweight: preserve navigation-site functionality and use explicit colors from the file, but do not attempt full AI-driven redesign.

## Precedence

1. `--design custom.DESIGN.md`
2. `--theme <built-in-theme>`
3. `ease`
