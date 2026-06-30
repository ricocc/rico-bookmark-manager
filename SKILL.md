---
name: rico-bookmark-manager
description: Browser bookmark management and organization: analyze, organize, deduplicate, check dead links, search, export, incrementally update, acquire browser bookmark data, or generate a local bookmark navigation site. Triggers in two cases, in any language: (1) the user mentions "rico" together with bookmark intent (rico is the entry keyword for the rico skill series); or (2) the user expresses a clear, specific browser-bookmark management task using concrete actions, such as organizing, deduplicating, checking dead links, exporting, incrementally updating, or building a navigation site from browser bookmarks. Do not trigger on vague or passing mentions of "bookmark/bookmarks" with no clear management action.
---

# Rico Bookmarks Manager

Use this skill to analyze, organize, update, and export browser bookmarks. The bundled CLI has stable file-based interfaces for browser-exported Netscape HTML files and existing `bookmarks.json` data. An AI/Agent may help acquire those input files from other sources when the user authorizes it and the environment supports it.

## First Principles Workflow

1. Clarify the user's goal: analyze, organize, deduplicate, check links, update incrementally, export, generate the navigation site, or inspect themes.
2. Identify the safest available input source: user-provided `bookmarks.html`, existing `bookmarks.json`, agent-visible files, or an authorized browser-data acquisition path.
3. Convert any non-standard source into a standard input file before invoking the CLI whenever practical.
4. Run the smallest command that satisfies the request. Prefer deterministic CLI behavior over ad hoc parsing.
5. Report what data was read, what files were written, and whether any browser profile, browser automation, or current-tab data was accessed.

## Decision Flow

1. Confirm the request either includes `rico` with bookmark intent, or expresses a clear, specific browser-bookmark management task (organizing, deduplicating, checking dead links, exporting, updating, or generating a navigation site). If it is only a vague or passing mention of bookmarks with no clear management action, do not use this skill implicitly.
2. Resolve the input source using the Input Acquisition Strategy below.
3. Identify the task:
   - Structure, duplicate, dead-link, search, or distribution analysis: read `references/cli.md`.
   - Organizing or reclassifying bookmarks: read `references/workflow.md` and `references/taxonomy.md`.
   - Incremental update into existing data: read `references/schema.md` and `references/workflow.md`.
   - Generating the local HTML bookmark navigation site: read `references/manager-spec.md`.
   - Selecting a built-in navigation theme or applying a provided `DESIGN.md`: read `references/design-md.md`.
4. Prefer the bundled script `scripts/rico_bookmarks_manager.py` for deterministic parsing, analysis, exports, and navigation-site generation.
5. For any generated user-facing surface, determine one display language before writing final output.

## Input Acquisition Strategy

- Prefer user-provided `bookmarks.html` for full runs, analysis, organization, and incremental update inputs.
- Prefer existing `bookmarks.json` for rebuilding the navigation site, exporting Markdown, exporting browser HTML, or merging a new export.
- If the user asks to get bookmarks from Chrome, Edge, Firefox, or another browser, inspect what the environment can safely access and explain the path you will use.
- The CLI public interface accepts standard files (`--input`, `--data`, `--existing`). If an agent obtains browser data through profile access, browser automation, or another tool, first convert or copy it into a standard intermediate file before calling the CLI whenever practical.
- Accessing browser profile files, automating a browser, or reading current open tabs requires explicit user intent and permission. Do not infer permission from a generic request like "整理书签" if browser data access is needed.
- If direct acquisition is unavailable, ask the user to export bookmarks from the browser and provide the HTML file.

## Agent Execution Policy

- Do not bind behavior to a specific agent product. Any environment that can read files, run Python, and write outputs can execute the core workflow.
- When a capable agent runtime offers browser automation or local file access, use it only as an input-acquisition layer; keep the processing pipeline centered on the bundled CLI and standard data files.
- Avoid promising that every agent can read local browser data. Capabilities depend on runtime permissions, OS access, browser state, and user approval.
- When reporting results, distinguish between CLI capabilities and external agent capabilities.

## Display Language Policy

- If the user explicitly names a display language, use that language.
- If the user does not specify a language, follow the main language of the current user request.
- If the display language is unclear, mixed, conflicts with the bookmark data language, or the user names an audience without a clear language, ask which language to use before generating the navigation site.
- Keep all template UI copy in a single language: headings, buttons, placeholders, aria labels, empty states, detail modal labels, export menu labels, and in-site Markdown/browser-export labels should not mix languages unless the user explicitly asks for bilingual output.
- For generated Markdown reports or summaries delivered to the user, localize report headings and explanatory prose to the same display language when needed, while preserving bookmark data values.
- Bookmark titles, URLs, domains, category names, tags, and source folder names are user data. Preserve them by default instead of translating them.
- The bundled CLI has no `--language` option. The bundled navigation template (`assets/bookmark-manager-template/index.html` and `app.js`) is **hardcoded in Chinese (zh)** by default. When the target display language differs, do not patch strings ad hoc: read `assets/bookmark-manager-template/i18n-strings.json` (a multilingual reference library covering every UI string in zh/en/ja/ko/es/fr), then for each key replace the template's current value with the target-language value. The `where` and current-`zh` value in each entry locate the string. Keep bookmark data intact, and keep the brand `Rico` / `Bookmarks` untranslated. If a needed language is missing from the library, add it to the JSON first, then apply. After localizing the template, run `manager` (or `all`) to generate the site.

## Required User Checkpoints

Before organizing, ask only for decisions that are not discoverable from files:

- Which input source to use if multiple are available: exported HTML, existing JSON, or an authorized agent-created intermediate file.
- Whether to output by original bookmark folders, optimized Rico taxonomy, or hybrid.
- Whether to use one, two, or three classification levels.
- Whether to generate all outputs or only browser import HTML, Markdown, navigation site, reports, or data.
- Whether this is a full run or an incremental update that should preserve existing classifications.
- Which navigation theme to use when generating HTML: `ease` by default, or one of the five built-in themes `kami`, `ease`, `minimal-mono`, `retro-blue`, `ui`, or a custom `--design` file. When offering choices, show all five built-in themes.
- Which display language to use, but only when the policy above cannot infer it confidently.

## Safety Defaults

- Do not edit Chrome/Edge/Firefox profile files directly.
- Do not access browser profile files, automate a browser, or read current tabs unless the user clearly wants that path and the environment permits it.
- Do not delete bookmarks automatically.
- Do not overwrite human-edited classifications during incremental updates.
- Treat navigation-site detail edits as browser-local staging by default. They do not write `bookmarks.json`; tell the user to export the adjusted JSON when they want a replacement data file.
- Put suspicious, duplicate, low-confidence, and dead-link items into reports for review.
- Use `--dry-run` before incremental writes when the user is checking behavior.
- Back up existing generated data before overwriting it.

## Quick Commands

```bash
python scripts/rico_bookmarks_manager.py analyze --input bookmarks.html --output rico-bookmarks
python scripts/rico_bookmarks_manager.py organize --input bookmarks.html --output rico-bookmarks --mode optimized --levels 2
python scripts/rico_bookmarks_manager.py export-html --data rico-bookmarks/data/bookmarks.json --output rico-bookmarks
python scripts/rico_bookmarks_manager.py export-md --data rico-bookmarks/data/bookmarks.json --output rico-bookmarks
python scripts/rico_bookmarks_manager.py themes
python scripts/rico_bookmarks_manager.py manager --data rico-bookmarks/data/bookmarks.json --theme kami --output rico-bookmarks/site
python scripts/rico_bookmarks_manager.py manager --data rico-bookmarks/data/bookmarks.json --theme ease --output rico-bookmarks/site
python scripts/rico_bookmarks_manager.py manager --data rico-bookmarks/data/bookmarks.json --theme minimal-mono --output rico-bookmarks/site
python scripts/rico_bookmarks_manager.py manager --data rico-bookmarks/data/bookmarks.json --theme retro-blue --output rico-bookmarks/site
python scripts/rico_bookmarks_manager.py manager --data rico-bookmarks/data/bookmarks.json --theme ui --output rico-bookmarks/site
python scripts/rico_bookmarks_manager.py manager --data rico-bookmarks/data/bookmarks.json --design DESIGN.md --output rico-bookmarks/site
python scripts/rico_bookmarks_manager.py update --input new.html --existing rico-bookmarks/data/bookmarks.json --output rico-bookmarks --dry-run
python scripts/rico_bookmarks_manager.py all --input bookmarks.html --output rico-bookmarks --theme kami
```
