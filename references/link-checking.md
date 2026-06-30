# Link Checking

Dead-link checks are optional network operations.

## Defaults

- Use a bounded thread pool.
- Try `HEAD` first, then fall back to `GET` for servers that reject `HEAD`.
- Treat 2xx and 3xx as reachable.
- Record redirects through `final_url`.
- Record 4xx/5xx as dead.
- Record timeout and connection failures separately.

## Safety

- Reuse cached results when available.
- Do not hammer one host with unbounded concurrency.
- Do not remove dead links automatically.
- Include dead links in reports and manager filters.
