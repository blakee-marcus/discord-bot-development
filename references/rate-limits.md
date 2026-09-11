# Rate Limits

**Checked on:** 2026-09-10
**Sources:**
- https://docs.discord.com/developers/topics/rate-limits
- https://docs.discord.com/developers/events/gateway#rate-limiting

## Global REST Rate Limit

- **50 requests per second** for bot global REST.
- Interaction endpoints are **excluded** from this limit.
- Exceeding returns 429 with `Retry-After` header.

## Per-Route Rate Limits

Some routes have stricter limits:
- **Application command creates**: 200 per day, per guild
- **Messages**: 5 messages per 5 seconds per channel
- **Thread creation**: stricter limits apply
- **Nickname changes**: 1 per second per guild

## Rate Limit Response Format

```json
{
  "message": "You are being rate limited.",
  "retry_after": 1.234,
  "global": false
}
```

### Headers

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Max requests per window |
| `X-RateLimit-Remaining` | Requests remaining in current window |
| `X-RateLimit-Reset` | When the window resets (Unix timestamp) |
| `X-RateLimit-Reset-After` | Seconds until reset |
| `X-RateLimit-Bucket` | Bucket ID for this route |
| `X-RateLimit-Global` | Whether this is a global limit |
| `X-RateLimit-Scope` | `user`, `global`, `resource` |

## 429 Handling

**Always honor `Retry-After`** before retrying.

### Implementation Pattern (Python)
```python
async def api_call_with_retry(request_func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await request_func()
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = e.retry_after  # or parse from response
                await asyncio.sleep(retry_after)
            else:
                raise
    raise Exception("Max retries exceeded")
```

### Implementation Pattern (JavaScript)
```javascript
async function apiCallWithRetry(requestFunc, maxRetries = 3) {
    for (let attempt = 0; attempt < maxRetries; attempt++) {
        try {
            return await requestFunc();
        } catch (error) {
            if (error.status === 429) {
                const retryAfter = error.retryAfter ?? 1;
                await new Promise(r => setTimeout(r, retryAfter * 1000));
            } else {
                throw error;
            }
        }
    }
    throw new Error("Max retries exceeded");
}
```

**Never use `time.sleep()` in async Python.** Always use `await asyncio.sleep()`.

## Invalid Request Threshold

- **10,000 responses** with status 401, 403, or 429 per 10 minutes.
- Shared-scope 429s are **excluded**.
- Exceeding this **invalidates your bot token**.
- Track invalid requests and stop retrying dead tokens or forbidden actions.

## Gateway Rate Limits

- **120 events per connection per 60 seconds** for sending.
- Exceeding disconnects the client.
- Heartbeats and ACKs are not counted.

## Concurrency Limits

- **1 IDENTIFY per 5 seconds** (session start limit).
- `GET /gateway/bot` returns `session_start_limit.remaining`.

## Drift Hazards

- Rate limit values change without notice.
- Discord adds new rate-limited routes.
- The `Retry-After` value is in seconds (float), not milliseconds.
- Global vs per-route limits behave differently.
- The invalid-request threshold (10,000 per 10 min) is a token-invalidating limit.
