# Gateway and Intents

**Checked on:** 2026-09-10
**Sources:**
- https://docs.discord.com/developers/events/gateway
- https://docs.discord.com/developers/events/gateway#gateway-intents
- https://docs.discord.com/developers/events/gateway#rate-limiting

## Gateway Lifecycle

The Gateway API lets apps open secure WebSocket connections to receive events
about actions in guilds.

### Connection Flow

1. **Identify**: Send an IDENTIFY payload with intents, shard info, and auth.
2. **Ready**: Receive READY with session info.
3. **Heartbeat**: Send heartbeat ACK at the interval specified in READY.
4. **Resume**: On disconnect, send RESUME with session_id and last sequence.
5. **Events**: Receive and process events.

### Session Start Limits

`GET /gateway/bot` returns sharding and session start limits:
- `shards`: recommended number of shards
- `session_start_limit`: max concurrent session starts

**Drift hazard**: Discord's docs state 120 events per connection per 60 seconds
for Gateway sending, but this limit can change. Always check the current
`session_start_limit` response.

## Gateway Intents

Intents are groups of events your bot subscribes to.

### Privileged Intents

| Intent | Bitwise | Description | Requirements |
|--------|---------|-------------|--------------|
| `GUILD_MEMBERS` | `1 << 1` | Guild member events | Verification for 100+ guilds |
| `GUILD_PRESENCES` | `1 << 8` | Presence/activity updates | Verification for 100+ guilds |
| `MESSAGE_CONTENT` | `1 << 14` | Message content | Verification for 100+ guilds |

**Known doc conflict**: Discord's privileged-intent thresholds and verification
requirements conflict across different doc pages. Always check the most current
thresholds before requesting privileged intents.

### Non-Privileged Intents

| Intent | Bitwise | Description |
|--------|---------|-------------|
| `GUILDS` | `1 << 0` | Guild events (create, update, delete) |
| `GUILD_MESSAGES` | `1 << 9` | Message events in guilds |
| `GUILD_MESSAGE_REACTIONS` | `1 << 10` | Reaction events |
| `DIRECT_MESSAGES` | `1 << 12` | DM events |
| `GUILD_VOICE_STATES` | `1 << 7` | Voice state updates |

**Slash-command-only bots**: Only need `GUILDS` and `GUILD_MESSAGES` (and
`MESSAGE_CONTENT` if you need message content, which is privileged).

## Sharding

Sharding is required when your bot reaches **2,500 guilds**.

- discord.js: `client.shard` or `ShardingManager`
- discord.py: `AutoShardedClient` or `discord.ext.commands.AutoShardedBot`

**Gateway sharding math**: Each shard receives events for a subset of guilds.
Total shards = `guild_count / 2500` rounded up.

## Heartbeats

- Send heartbeat ACK at the interval specified in READY (typically 41,250ms).
- Missed heartbeats result in session invalidation.
- The Gateway sends a HEARTBEAT ACK in response.

## Resume

On disconnect:
1. Wait for a new connection.
2. Send RESUME payload with `session_id`, `token`, and `seq` (last sequence).
3. If RESUME fails, send a fresh IDENTIFY.

## Rate Limiting (Gateway)

- **120 events per connection per 60 seconds** for sending.
- Exceeding this disconnects the client.

## Drift Hazards

- Sharding threshold (2,500 guilds) has changed before.
- Privileged intent thresholds change; check current values.
- The Gateway URL is `wss://gateway.discord.gg/?v=10&encoding=json` (v10 is current).
- `compress` option is supported; `zlib-stream` is the compression method.
