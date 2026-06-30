# CLI Reference

Use `scripts/rico_bookmarks_manager.py` for repeatable bookmark processing.

## Commands

| Command | Purpose |
| --- | --- |
| `analyze` | Parse a browser HTML export, then report structure, duplicates, distribution, dead links when requested, and optimization suggestions. |
| `organize` | Parse and classify bookmarks into source, optimized, or hybrid category paths. |
| `export-html` | Generate browser-importable Netscape Bookmark File Format HTML from an existing data file. |
| `export-md` | Generate overview, category Markdown files, and reports from an existing data file. |
| `manager` | Generate a local static bookmark navigation site from an existing data file. |
| `update` | Merge only new bookmarks from a fresh HTML export into an existing `bookmarks.json`. |
| `all` | Run organize, Markdown export, browser import HTML export, and navigation-site generation. |
| `themes` | List built-in HTML navigation themes. |

## Common Options

- `--input`: Browser-exported HTML file.
- `--output`: Output folder. Use `rico-bookmarks` for project runs.
- `--data`: Existing `bookmarks.json` data file.
- `--existing`: Existing `bookmarks.json` for incremental update.
- `--mode source|optimized|hybrid`: Classification mode.
- `--levels 1|2|3`: Maximum category depth.
- `--check-links`: Run dead-link detection.
- `--no-network`: Skip network checks.
- `--dry-run`: Preview update writes without changing data files.
- `--design DESIGN.md`: Apply visual tokens from a custom design reference when generating the navigation site.
- `--theme kami|ease|minimal-mono|retro-blue|ui`: Pick one built-in navigation theme. Defaults to `ease`.

When presenting built-in theme choices to a user or in a generated test prompt, include all five options: `kami`, `ease`, `minimal-mono`, `retro-blue`, `ui`.

Built-in theme CSS files live at `assets/themes/<theme-id>/theme.css`. The manager copies that file when present and falls back to generating it from `theme.json` if it is missing. Custom `--design` output still generates `theme.css` at build time.

## Display Language

The CLI intentionally has no `--language` option and no built-in language packs. When an AI uses this skill, it should determine the navigation site's single display language from the user's request, ask when unclear, and localize generated template copy after running the script if the default template language is not appropriate. Bookmark data itself should stay unchanged unless the user asks for translation.

## Navigation-Site Edits

The generated navigation site is static. Detail-panel edits are browser-local staging saved in `localStorage`, not writes to `bookmarks.json`. Use the JSON export inside the site to download data that includes staged category, tag, and description changes.

## Examples

```bash
python scripts/rico_bookmarks_manager.py analyze --input bookmarks.html --output rico-bookmarks
python scripts/rico_bookmarks_manager.py organize --input bookmarks.html --output rico-bookmarks --mode optimized --levels 2
python scripts/rico_bookmarks_manager.py themes
python scripts/rico_bookmarks_manager.py manager --data rico-bookmarks/data/bookmarks.json --theme kami --output rico-bookmarks/site
python scripts/rico_bookmarks_manager.py manager --data rico-bookmarks/data/bookmarks.json --theme ease --output rico-bookmarks/site
python scripts/rico_bookmarks_manager.py manager --data rico-bookmarks/data/bookmarks.json --theme minimal-mono --output rico-bookmarks/site
python scripts/rico_bookmarks_manager.py manager --data rico-bookmarks/data/bookmarks.json --theme retro-blue --output rico-bookmarks/site
python scripts/rico_bookmarks_manager.py manager --data rico-bookmarks/data/bookmarks.json --theme ui --output rico-bookmarks/site
python scripts/rico_bookmarks_manager.py manager --data rico-bookmarks/data/bookmarks.json --design custom.DESIGN.md --output rico-bookmarks/site
python scripts/rico_bookmarks_manager.py all --input bookmarks.html --output rico-bookmarks --theme kami --no-network
python scripts/rico_bookmarks_manager.py update --input new.html --existing rico-bookmarks/data/bookmarks.json --output rico-bookmarks --dry-run
```

## Intent Mapping

- "rico 查看书签结构" -> `analyze --input ...`
- "rico 查重复书签" -> `analyze --input ...`
- "rico 检查死链" -> `analyze --input ... --check-links`
- "rico 只导出 markdown" -> `export-md --data ...`
- "rico 只输出浏览器导入 html" -> `export-html --data ...`
- "rico 增量更新书签" -> `update --input new.html --existing ... --dry-run`
- "rico 查看内置主题" -> `themes`
- "rico 用 Kami 生成书签导航站" -> `manager --data ... --theme kami`
- "rico 用 Ease 生成书签导航站" -> `manager --data ... --theme ease`
- "rico 用 Minimal Mono 生成书签导航站" -> `manager --data ... --theme minimal-mono`
- "rico 用 Retro Blue 生成书签导航站" -> `manager --data ... --theme retro-blue`
- "rico 用 UI Swiss Grid 生成书签导航站" -> `manager --data ... --theme ui`
- "rico 生成书签导航站并按 DESIGN.md 优化" -> `manager --data ... --design DESIGN.md`
