# Sharding and Operations

**Checked on:** 2026-09-10
**Sources:**
- https://docs.discord.com/developers/events/gateway#sharding
- https://discordjs.guide/sharding/
- https://discordpy.readthedocs.io/en/stable/api.html#sharding

## Sharding Requirements

Sharding is **required** when your bot reaches **2,500 guilds**.

- Each shard receives events for a subset of guilds.
- Total shards = `guild_count / 2500` rounded up.
- `GET /gateway/bot` returns the recommended shard count.

## Sharding in discord.js

### ShardingManager

```javascript
const { ShardingManager } = require('discord.js');
const manager = new ShardingManager('./bot.js', {
    token: process.env.DISCORD_TOKEN,
    totalShards: 'auto',  // or specific number
});

manager.on('shardCreate', shard => console.log(`Launched shard ${shard.id}`));
manager.spawn();
```

### Bot File (per shard)

```javascript
const { Client, GatewayIntentBits } = require('discord.js');
const client = new Client({
    intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages],
});

client.login(process.env.DISCORD_TOKEN);
```

## Sharding in discord.py

### AutoShardedClient

```python
import discord
from discord.ext import commands

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=discord.Intents.default(),
            shard_count='auto',  # or specific number
        )

bot = MyBot()
bot.run(os.environ['DISCORD_TOKEN'])
```

### Manual Sharding

```python
import discord

class MyClient(discord.Client):
    def __init__(self, shard_id, shard_count):
        super().__init__(intents=discord.Intents.default())
        self.shard_id = shard_id
        self.shard_count = shard_count

client = MyClient(shard_id=0, shard_count=2)
client.run(os.environ['DISCORD_TOKEN'])
```

## Process Managers

Use a process manager for production:

### PM2 (Node.js)
```bash
pm2 start bot.js --name discord-bot
pm2 save
pm2 startup
```

### systemd (Linux)
```ini
[Unit]
Description=Discord Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/opt/discord-bot
ExecStart=/usr/bin/node bot.js
Restart=always
RestartSec=10
Environment=DISCORD_TOKEN=your_token

[Install]
WantedBy=multi-user.target
```

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
CMD ["node", "bot.js"]
```

## Graceful Shutdown

### discord.js
```javascript
process.on('SIGINT', async () => {
    console.log('Shutting down...');
    await client.destroy();
    process.exit(0);
});
```

### discord.py
```python
import signal
import sys

async def shutdown():
    await bot.close()

def handle_signal(sig, frame):
    asyncio.create_task(shutdown())
    sys.exit(0)

signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)
```

## Durable State

**Never store counters, rate-limit state, or queued work in process memory.**

Use persistent storage:
- **Redis**: fast key-value, rate-limit counters
- **PostgreSQL**: relational data, command state
- **SQLite**: simple deployments, local state

## Observability

### Metrics to Track

| Metric | Description |
|--------|-------------|
| `ack_latency_ms` | Time to ACK/defer interactions |
| `response_failures` | Failed interaction responses |
| `rate_limits_hit` | 429 responses received |
| `shard_reconnects` | Gateway reconnect count |
| `invalid_sessions` | Invalid session events |
| `command_version` | Current command version deployed |

### Logging

```javascript
// discord.js
client.on('debug', console.log);
client.on('warn', console.warn);
client.on('error', console.error);
```

```python
# discord.py
import logging
logging.basicConfig(level=logging.INFO)
```

## Test-Guild Strategy

- Use a **separate application** for testing.
- Use a **separate guild** for test commands.
- **Never use a production token or production guild in CI.**
- Guild commands update instantly — ideal for development.

## Drift Hazards

- Sharding threshold (2,500 guilds) has changed before.
- `GET /gateway/bot` response format can change.
- Process manager configurations vary by OS.
- Docker base images change; pin versions.
