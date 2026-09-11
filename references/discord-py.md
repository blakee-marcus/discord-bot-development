# discord.py Reference

**Checked on:** 2026-09-10
**Sources:**
- https://discordpy.readthedocs.io/en/stable/
- https://pypi.org/project/discord.py/
- https://raw.githubusercontent.com/Rapptz/discord.py/master/pyproject.toml

## Version Snapshot

| Field | Value |
|-------|-------|
| Version | **2.7.1** |
| Released | 2026-03-03 |
| Python | >=3.8 |
| Status | Stable |

## Installation

```bash
pip install discord.py
# or
pip install "discord.py[voice]"  # with voice support
```

## Client Setup

```python
import discord
from discord.ext import commands

bot = commands.Bot(
    command_prefix='!',
    intents=discord.Intents.default(),
)
```

### Custom Intents

```python
intents = discord.Intents.default()
intents.message_content = True  # Privileged
intents.members = True          # Privileged
intents.presences = True        # Privileged

bot = commands.Bot(
    command_prefix='!',
    intents=intents,
)
```

## Application Commands (app_commands)

### Setup

```python
import discord
from discord import app_commands

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
```

### Commands

```python
@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {bot.latency*1000:.0f}ms")
```

### Guild Commands (dev)

```python
guild = discord.Object(id=TEST_GUILD_ID)

@bot.tree.command(name="test", description="Test command", guild=guild)
async def test_cmd(interaction: discord.Interaction):
    await interaction.response.send_message("Test!")
```

## Interaction Lifecycle

```python
@bot.tree.command(name="echo", description="Echo a message")
async def echo(interaction: discord.Interaction, message: str):
    # ACK within 3 seconds
    await interaction.response.send_message(f"You said: {message}")
```

### Defer

```python
@bot.tree.command(name="slow", description="Slow command")
async def slow(interaction: discord.Interaction):
    # Defer for work > 3 seconds
    await interaction.response.defer()
    await asyncio.sleep(5)
    await interaction.followup.write("Done!")
```

### Follow-up

```python
@bot.tree.command(name="multi", description="Multiple responses")
async def multi(interaction: discord.Interaction):
    await interaction.response.send_message("First")
    await interaction.followup.send("Second")
```

## Checks and Permissions

### Default Permissions

```python
@app_commands.default_permissions(manage_messages=True)
@bot.tree.command(name="mod", description="Moderator command")
async def mod_cmd(interaction: discord.Interaction):
    await interaction.response.send_message("Mod only")
```

### Check Decorator

```python
@app_commands.checks.has_role("Admin")
@bot.tree.command(name="admin", description="Admin command")
async def admin_cmd(interaction: discord.Interaction):
    await interaction.response.send_message("Admin only")

@admin_cmd.error
async def admin_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingRole):
        await interaction.response.send_message("You need Admin role", ephemeral=True)
```

## Error Handling

```python
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission!")
    else:
        raise error
```

## Background Tasks

```python
from discord.ext import tasks

@tasks.loop(minutes=5)
async def my_task():
    print("Running background task...")

@my_task.before_loop
async def before_my_task():
    await bot.wait_until_ready()

my_task.start()
```

**Never use `time.sleep()` in tasks** — use `await asyncio.sleep()`.

## Cogs

```python
class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello!")

async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

## Graceful Shutdown

```python
@bot.event
async def on_disconnect():
    print("Disconnected, will resume...")

@bot.event
async def on_resumed():
    print("Resumed!")

async def shutdown():
    await bot.close()

# Register signal handlers
import signal
signal.signal(signal.SIGTERM, lambda: asyncio.create_task(shutdown()))
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `client.run(token)` with token in code | `bot.run(os.environ['DISCORD_TOKEN'])` |
| `client.event` without `async` | Event handlers must be `async def` |
| `time.sleep()` in async | Use `await asyncio.sleep()` |
| `tree.sync()` in `on_ready` | Call in `setup_hook` once |
| `await` outside async function | All discord.py callbacks are async |
| `discord.Client()` without intents | `discord.Intents.default()` or custom |
| `client.login()` without `run()` | Use `bot.run()` for proper loop handling |
| Cog setup without `await bot.add_cog()` | Use `await bot.add_cog(Cog(bot))` |
| `ctx.send()` without `await` | All API calls are coroutines |
| `interaction.response.send_message()` twice | Use `is_done()` guard or `followup` |
| `bot.tree.sync()` without guild param | Specify guild for dev, no guild for global |
| Missing `setup_hook` for sync | Use `async def setup_hook(self): await self.tree.sync()` |
| `discord.ext.commands.Bot()` without command_prefix | Required argument |

## Drift Hazards

- discord.py 2.x is the stable line; 1.x is legacy.
- `asyncio` event loop handling changed in Python 3.10+.
- The `master` branch may differ from published 2.7.1.
- `setup_hook` replaced `on_ready` for sync (recommended).
- `app_commands` is the modern approach; `commands.Context` is legacy.
- The `discord.py` library is community-maintained; no official Discord support.
