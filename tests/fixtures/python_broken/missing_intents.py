# python_broken/missing_intents.py — DB012 positive fixture
# This file creates Bot without explicit intents (BAD - discord.py 2.x requires it)

from discord.ext import commands

# BAD: No intents parameter (discord.py 2.x requires this)
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

bot.run('a.b.c')
