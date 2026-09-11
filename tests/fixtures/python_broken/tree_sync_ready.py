# python_broken/tree_sync_ready.py — DB010 positive fixture
# This file calls tree.sync() in on_ready (BAD)

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.event
async def on_ready():
    # BAD: tree.sync() in on_ready
    await bot.tree.sync()
    print(f'Logged in as {bot.user}')

bot.run('a.b.c')
