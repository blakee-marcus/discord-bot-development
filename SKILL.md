---
name: discord-bot-development
description: "Build production-quality Discord bots correctly. Framework-aware (discord.js 14.27, discord.py 2.7) but fundamentals-first: application setup, Gateway intents, interactions/slash commands, permissions, rate limits, OAuth2, security, sharding, testing, and deployment."
version: 0.1.0
author: Blake Marcus
license: MIT
homepage: https://github.com/blakee-marcus/discord-bot-development
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [discord, discord-bot, discord-js, discord-py, slash-commands, gateway, intents, interactions, agent-skill]
    homepage: https://github.com/blakee-marcus/discord-bot-development
---

# Discord Bot Development

A source-backed agent skill for building **production-quality Discord bots**. It
teaches the platform fundamentals so agents build bots correctly the first time,
and audits bot code for the mistakes LLMs repeatedly make. It is documentation
plus a deterministic checker, **not a bot runtime**: it describes the Discord API
surface; it does not run a bot.

## When to Use

- Building a new Discord bot from scratch (Node/TypeScript or Python)
- Adding slash commands, message components, modals, or context menus
- Registering commands via REST (global or guild-scoped)
- Auditing an existing bot for security, permissions, or rate-limit mistakes
- Migrating a bot to current stable discord.js / discord.py
- Deploying a bot to production (process manager, graceful shutdown, observability)

**Don't use for:** non-Discord platforms, actual bot runtime/execution, trading
systems, credential management, or anything requiring a live bot token. This
skill ships no bot runtime.

## What It Will NOT Do

- It will **not** run, host, or execute a Discord bot.
- No bot tokens, API keys, or credentials. It will not ask you to paste them.
- No live Discord API calls during instruction. All examples are offline or
  read-only unless explicitly building a real bot (which is outside this skill's
  verification scope).
- No reads/writes of any private repo, notes, chat logs, or internal system.

## Authority Order

1. Current official Discord developer docs (`docs.discord.com`)
2. Current framework docs: discord.js (`discordjs.guide`,
   `discord.js.org/docs/packages/discord.js/14.27.0`), discord.py
   (`discordpy.readthedocs.io/en/stable`)
3. Observed API behavior when it diverges from the docs
4. This skill's reference pages
5. Prior implementations, only when explicitly consulted

**Discord's docs are schema authority.** If a reference page disagrees with a
published spec, the spec wins and the page should be corrected.

## Workflow (every request)

1. **Detect** — Which framework? Which version? What pipeline
   (Vite/PostCSS/CLI-equivalent for Discord: gateway vs HTTP vs webhook)? What
   intents? What permissions? What command scope?
2. **Classify** — Task type: new bot / add feature / migrate / audit / debug
3. **Design** — Choose the right interaction type, registration path,
   intent set, and permission bitmap. Prefer least privilege.
4. **Implement** — Follow the framework reference. REST-only registration.
   ACK/defer within 3 seconds. Honor `Retry-After` on 429.
5. **Verify** — Run the checker, lint, typecheck, and test matrix. Confirm
   command registration path exists and is reachable.

## Procedure (handle a request)

1. Pick the right reference(s) from the inventory below.
2. For **audit**: run `scripts/discord_doctor.py <path>`; report each FAIL/WARN
   with file:line, rule id, official source, and fix.
3. For a **how-to**: answer from references; cite the official URL.
4. Verify any claim against current docs — Discord's privileged-intent and
   verification thresholds conflict across docs; surface, don't silently
   resolve (see `references/security-and-policy.md`).
5. Never issue a state-changing API call from this skill. If the user wants a
   real bot built, that is a separate project with its own execution boundary.

## Version Snapshots (drift-sensitive)

| Framework | Version | Released | Runtime | Tag |
|-----------|---------|----------|---------|-----|
| discord.js | **14.27.0** | 2026-07-15 | Node >=18 (package); Node >=22.12.0 recommended by guide | Stable |
| discord.py | **2.7.1** | 2026-03-03 | Python >=3.8 | Stable |

discord.js v15 is **pre-release** — do not generate production code against it.
discord.py pre-2.0 patterns are legacy — avoid.

## Core Rules (non-negotiable)

- **3-second ACK/defer**: send an initial interaction response or defer within
  3 seconds or the interaction token invalidates. Use `DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE`
  (callback type 5) for work that cannot finish in time.
- **15-minute token validity**: interaction tokens are valid for 15 minutes for
  edits and follow-ups.
- **Exact-one initial response**: a given interaction can be acknowledged exactly
  once. Use `is_done()` guards before any response method.
- **Guild commands for dev, global for release**: guild commands update
  instantly; global commands propagate up to 1 hour. Develop with guild scope,
  then bulk-overwrite to global for release.
- **REST-only registration**: application commands are registered only via HTTP
  endpoints, never over the Gateway.
- **Least-privilege intents**: request only the intents your bot needs.
  `MESSAGE_CONTENT` is privileged and requires verification for 100+ guilds.
- **Least-privilege permissions**: compute the minimal permission bitmap. Use
  `default_permissions` and installation contexts.
- **Runtime authorization**: check permissions, channel overwrites, and role
  hierarchy — never trust `customId`, cached members, or client state alone.
- **allowed_mentions**: set explicitly to avoid unexpected pings.
- **Raw-body Ed25519 webhook verification**: validate `X-Signature-Ed25519`
  and `X-Signature-Timestamp` over the exact raw body for interaction endpoints.
- **Secrets/redaction**: tokens in environment variables or managed secret store,
  never in code or logs. Redact on any error path.
- **Rate limits**: honor `Retry-After` / `retry_after` on 429. Global REST is
  50 req/s (interaction endpoints excluded). Gateway sending is 120 events per
  connection per 60s. Invalid-request threshold: 10,000 responses with
  401/403/429 per 10 minutes.
- **No hard-coded sleeps**: never use `time.sleep()` in async Python; never
  busy-wait in JS.
- **Gateway**: heartbeat ACK, resume on disconnect, track sequence numbers.
  Use `GET /gateway/bot` for sharding/session-start limits.
- **Sharding**: required at 2,500 guilds. discord.js uses `ShardingManager`;
  discord.py uses `AutoShardedClient`.
- **Durable state**: keep counters, rate-limit state, and queued work in
  persistent storage, not in-memory collectors or process memory.
- **Graceful shutdown**: drain in-flight interaction work, preserve resume state.
- **Observability**: metrics for ACK latency, response failures, rate limits,
  shard reconnects, invalid sessions, and command-version rollout.

## Reference Files

- `references/application-setup.md` — application/bot creation, installation
  contexts, public key, token handling
- `references/interactions-and-commands.md` — slash commands, message/user
  commands, message components, modals, autocomplete, contexts
- `references/gateway-and-intents.md` — Gateway lifecycle, intents (privileged
  and not), sharding, session limits, resume, heartbeat
- `references/permissions-and-oauth2.md` — permission bitmaps, installation
  contexts, OAuth2 flows, scopes, default permissions
- `references/rate-limits.md` — REST limits, Gateway limits, 429 handling,
  `Retry-After`, invalid-request threshold, concurrency
- `references/security-and-policy.md` — webhook signature verification,
  secrets, allowed_mentions, data handling, privileged intent thresholds,
  known doc conflicts
- `references/sharding-and-operations.md` — sharding requirements, process
  managers, graceful shutdown, deployment, test-guild strategy
- `references/testing-and-deployment.md` — unit/integration tests, mocks,
  test-guild smoke tests, CI, deployment pipelines
- `references/discord-js.md` — discord.js 14.27 stable patterns, REST/Gateway
  separation, collectors/components/modals, cache sweepers, common mistakes
- `references/discord-py.md` — discord.py 2.7 stable patterns, app_commands,
  tasks, checks, error handling, blocking-I/O pitfalls, common mistakes
- `references/official-sources.md` — canonical URL inventory, checked-on date,
  drift hazards, changelog review checklist

## Checker

```bash
discord-doctor <path-to-bot>           # PASS/WARN/FAIL report
discord-doctor <path> --json          # machine-readable
discord-doctor --rules               # list rule IDs
discord-doctor --version             # show version
```

Legacy invocation still works via the compatibility wrapper:

```bash
python scripts/discord_doctor.py <path-to-bot>
```

Run `pytest tests/` for the full test suite, including checker fixture tests.

## Pitfalls (verified, source-backed)

- ❌ Embedding a bot token in source code or printing it in logs
- ❌ Registering commands inside a `ready` / `on_ready` handler (race, duplicates)
- ❌ Forgetting to construct the client with required intents
- ❌ Using `time.sleep()` in async Python; busy-wait in JS
- ❌ Calling `tree.sync()` from `on_ready` (discord.py)
- ❌ Requesting `MESSAGE_CONTENT` without needing it (privileged)
- ❌ Permanent in-memory collectors/components without cleanup or timeout
- ❌ Trusting `customId` / cached members without authorization
- ❌ Retrying 403/404/429 responses indefinitely without honoring `Retry-After`
- ❌ Assuming caches are complete (they aren't)
- ❌ Using deprecated v12/v13 discord.js APIs or pre-2.0 discord.py patterns
- ❌ Running unit tests against a production token or production guild
- ❌ Gateway and outgoing webhook on the same application (mutually exclusive)

## License

MIT — see `LICENSE`.
