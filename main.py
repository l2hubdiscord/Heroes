import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # Αν θες να απαντάει σε μηνύματα

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot connected as {bot.user}")

# Dummy command για να ελέγξεις ότι λειτουργεί
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Token από περιβάλλον (Koyeb env vars)
bot.run(os.environ["TOKEN"])
