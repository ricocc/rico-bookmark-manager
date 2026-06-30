# Data Schema

The script writes a JSON object with `bookmarks`, `reports`, `taxonomy`, and run metadata.

## Bookmark Record

```json
{
  "id": "canonical-url-hash",
  "title": "Bookmark title",
  "url": "Original URL",
  "canonical_url": "Normalized URL for matching",
  "final_url": "Final URL after redirects, when checked",
  "domain": "example.com",
  "source_folder_path": ["Bookmarks Bar", "AI"],
  "category_path": ["AI", "AI工具"],
  "source_category_path": ["Bookmarks Bar", "AI"],
  "optimized_category_path": ["AI", "AI工具"],
  "tags": ["AI", "AI工具", "OpenAI"],
  "description": "Short description",
  "http_status": 200,
  "link_status": "alive | dead | redirected | timeout | error | unknown",
  "duplicate_group": "hash or null",
  "confidence": 0.86,
  "review_status": "kept | low_confidence | duplicate | dead_link | filtered_candidate"
}
```

## Update Rules

- Match existing bookmarks by `canonical_url`.
- Preserve existing human-reviewed fields.
- Add new bookmarks with fresh classification.
- Report title or source-folder changes without overwriting review fields.
- Backup existing data before writing unless `--dry-run` is used.
