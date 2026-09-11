# python_ok/clean_bot.py — negative fixture (should PASS)
# This file demonstrates clean discord.py 2.7 patterns

import discord
from discord.ext import commands
import os

# GOOD: Explicit intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.tree.command(name="ping", description="Ping command")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

# GOOD: No hardcoded token
bot.run(os.environ['DISCORD_TOKEN'])
