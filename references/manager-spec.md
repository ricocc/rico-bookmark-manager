# HTML Bookmark Navigation Site Spec

Generate a local static bookmark navigation site under `site/`. The first screen should feel like a useful personal navigation website, not an admin workbench.

## Primary Experience

- Home: brand, global search, category entry points, featured bookmarks, stats, and full library.
- Library: grid cards by default, compact list as an alternate view.
- Browse filters: first-level category, second-level category, tag, domain, link status, and search query.
- Bookmark cards: title, domain, category path, real tags when present, short description, visit action, and secondary detail action.
- Detail modal: URL, optimized category path, source folder path, real tags, status, description, and optional local adjustment controls.
- Reports: duplicates, dead links, distribution, and suggestions live under a secondary report dialog.

## Single-Language Output

- Use exactly one display language for all template UI copy in a generated navigation site unless the user explicitly asks for bilingual output.
- Determine display language from the user's explicit instruction first, then from the main language of the current request.
- If the target display language is unclear, mixed, conflicts with bookmark data language, or depends on an unspecified audience, ask the user which language to use before generating the site.
- Do not add a `--language` CLI option, built-in language packs, or a fixed country/language list. Language choice is handled by the AI executing the skill.
- The default bundled template is an English single-language base. If the user's target display language differs, localize the generated `index.html` and `app.js` template copy after generation.
- Localize user-facing template copy: titles, headings, labels, buttons, placeholders, aria labels, empty states, result counts, detail modal labels, report dialog labels, export menu labels, and in-site Markdown/browser-export labels.
- Preserve bookmark titles, URLs, domains, category names, tags, source folder paths, and status values by default. They are user data, not template copy.

## Display Rules

- Show only real tags from bookmark data. Do not invent fallback tags and do not show `unknown`, empty, `undefined`, or placeholder tags.
- If a bookmark has no tags, hide the card tag row.
- Hide optional metadata when absent unless a quiet fallback helps comprehension, such as "未检测" for link status in detail view.
- Long titles, URLs, category paths, and tags must truncate or wrap without breaking the layout.
- Clicking the main card opens the bookmark. The detail button opens metadata without making the page feel like a backend tool.

## Required Controls

- Text search across title, URL, domain, description, tags, source path, and category path.
- Filters for category, subcategory, tag, domain, and link status.
- Grid/list toggle.
- Collapsible desktop sidebar with an icon button. On mobile, keep the compact header and mobile tool buttons instead of duplicating the desktop sidebar collapse behavior.
- Lightweight guide dialog opened from a `circle-help` icon. It should explain search/filtering, bookmark actions, reports/exports, and local staging without auto-opening on page load.
- Export JSON, Markdown summary, and browser import HTML from local data.
- Local staging for category, tag, and description edits using `localStorage`, placed in the detail modal or another advanced surface.
- Mobile must keep first-class access to filters, reports, and export through compact tool buttons; do not hide these workflows when the sidebar collapses.

## Visual Direction

- The default template should read as a directory atlas: structured, index-like, scan-friendly, and useful for repeated navigation.
- Favor data state over generic marketing copy. Show counts, result status, problem-link signals, and staged-edit counts where they help orientation.
- Bookmark cards should emphasize title and domain first, description second, and category/tags/status as quieter metadata.
- Site icons should be deterministic local marks, such as domain-initial badges with stable colors, instead of relying on network favicon fetching.
- Keep the experience static and restrained: no landing-page hero, no decorative imagery, and no runtime theme switcher.
- Use solid or softly tinted surfaces for the page background. Avoid page-level grid, dot, or patterned backgrounds behind the main content.

## Local Staging Edits

- The generated navigation site is static and must not imply that it can write back to `bookmarks.json`.
- Label advanced editing as local staging. Explain that changes are saved only in the current browser.
- Provide a reset action for each staged bookmark so the user can clear local changes.
- Exported JSON must include staged category, tag, and description changes so the user can intentionally replace the source data if desired.
- Do not add a local server or source-file writeback flow unless the user explicitly asks for a full editable local app.

## Theme System

Use build-time theming. The generated manager loads `styles.css` for layout and `theme.css` for semantic variables. Do not include runtime theme switching.

Built-in themes keep a pre-generated `theme.css` beside each `theme.json` under `assets/themes/<theme-id>/`. When generating a site with `--theme`, copy that CSS into the output if it exists; if it is missing, generate `theme.css` from `theme.json`. Custom `--design` themes are always generated at build time.

Built-in theme choices: `kami`, `ease`, `minimal-mono`, `retro-blue`, `ui`. When the AI asks the user to choose a built-in theme, present all five choices.

Semantic variables:

- Surfaces: `--bg`, `--panel`, `--panel-raised`, `--sidebar`, `--overlay`
- Text: `--text`, `--muted`, `--faint`, `--inverse`
- Actions: `--accent`, `--accent-strong`, `--accent-soft`
- States: `--danger`, `--warning`, `--success`
- Structure: `--border`, `--shadow`, `--radius-sm`, `--radius-md`, `--radius-pill`
- Typography: `--font-ui`, `--font-display`, `--font-mono`

Default theme: `ease`.

## Icon System

The navigation site uses [lucide](https://lucide.dev) icons for the sidebar, view toggles, search, modals, cards, and the insights toolbar — anywhere a glyph is needed.

- Load lucide from a **pinned** CDN URL in `index.html`, before `app.js`. Pinning keeps generated sites reproducible:
  ```html
  <script src="https://unpkg.com/lucide@0.460.0/dist/umd/lucide.js"></script>
  ```
  Bump the version deliberately; the `lucide.createIcons()` API and `[data-lucide]` convention are stable across 0.x/1.x.
- Author icons as `<i data-lucide="icon-name" class="icon"></i>`. The `icon` class sizes them to `1em`; add a second class (e.g. `cat-icon`) for specific sizes.
- Icons in **static** markup (search, view toggle, close, sidebar labels, buttons, insight tabs) are converted once at init.
- Icons in **JS-rendered** markup (category nav, cards, detail modal, insights panels) must be re-converted after every `innerHTML` write. Call the bundled `refreshIcons()` helper (which no-ops when lucide is unavailable) at the end of each render pass — the template already does this in `renderAll`, `renderInsights`, and `showDetail`.
- Degrade gracefully: if lucide fails to load (offline), `[data-lucide]` elements stay empty and the layout still works. Never put essential information only inside an icon.

Icons currently used in the template: `search`, `layout-grid`, `list`, `folder`, `hash`, `globe`, `activity`, `bar-chart-3`, `download`, `external-link`, `copy`, `link-2`, `lightbulb`, `sliders-horizontal`, `circle-help`, `chevron-left`, `chevron-right`, `x`.

### Category Icons

The `categoryIcon(name)` function in `app.js` maps each category to a distinct lucide icon so the sidebar is visually differentiated instead of showing `folder` everywhere.

**Top-level exact map:**

| Category | Icon |
|---|---|
| AI | `sparkles` |
| 前端 | `code-2` |
| 设计 | `palette` |
| 互联网 | `compass` |
| 工具产品 | `wrench` |
| 博客 | `pen-tool` |
| 学习教程 | `graduation-cap` |
| 其他 | `shapes` |

**Keyword fallback** (for dynamically-created subcategories): the function tests the category name against a list of regex patterns — e.g. `web3|crypto|nft` → `bitcoin`, `3d|webgl|motion` → `box`, `作品集|portfolio` → `user`, `品牌|brand` → `badge-check`, `灵感|inspiration` → `images`, `字体|font` → `type`, `配色|color` → `pipette`, `电商|shop` → `shopping-bag`, `支付|payment` → `credit-card`. Unmatched names fall back to `hash`.

Icons are applied to:
- Top-level category nav items (`.cat-icon` class).
- Subcategory nav rows (`.cat-subitem .cat-icon`, 13px, muted).
- Path-pills in bookmark cards and rows (`categoryIcon(categoryPath[0])`).

All icons are converted by the existing `refreshIcons()` calls — no new wiring needed.
