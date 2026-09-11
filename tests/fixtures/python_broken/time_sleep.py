# python_broken/time_sleep.py — DB009 positive fixture
# This file uses time.sleep() in async context (BAD)
# WARNING: The token below is intentionally fake and for testing only

import discord
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    # BAD: Using time.sleep() in async context
    await ctx.send('Waiting...')
    # Should use: await asyncio.sleep(1)
    import time
    time.sleep(1)
    await ctx.send('Pong!')

# BAD: Literal token (fake token for testing only)
bot.run('FAKE_TOKEN_FOR_TESTING_ONLY_1234567890abcdef1234567890abcdef1234567890')
