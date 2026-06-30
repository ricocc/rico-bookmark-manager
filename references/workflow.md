# Workflow

## Full Run

1. Parse the browser HTML export.
2. Generate a preflight analysis: folder tree, counts, duplicate groups, domain distribution, and "other" concentration.
3. If `其他/待确认` concentration is high, the export's domain is not well covered by the built-in taxonomy. Extend classification for this dataset — name categories and add matching rules per `references/taxonomy.md` — then re-run the preflight to confirm `其他` drops before finalizing.
4. Ask whether to use:
   - `source`: original browser folders.
   - `optimized`: Rico taxonomy.
   - `hybrid`: preserve original paths while exporting optimized category paths.
4. Ask for max depth: 1, 2, or 3 levels.
5. Run organization.
6. Generate requested outputs: data, reports, Markdown, browser import HTML, and/or manager.

## Incremental Update

1. Load existing `bookmarks.json`.
2. Parse new browser HTML.
3. Normalize URLs and compare against existing canonical URLs.
4. Preserve existing category paths, tags, descriptions, review status, and human edits.
5. Classify only new items.
6. Produce `reports/增量更新.md` with added, duplicate, changed-title, and skipped counts.
7. Use `--dry-run` first when the user asks to preview.

## Conservative Review Rules

- Never delete automatically.
- Keep duplicate groups in reports.
- Keep dead links in data with `link_status`.
- Mark low-confidence classifications as `review_status: low_confidence`.
- Keep "其他" when confidence is low instead of inventing a misleading category.
