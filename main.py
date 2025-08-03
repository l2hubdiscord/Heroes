import os
import discord
from discord.ext import commands
from threading import Thread
from flask import Flask

# 🔧 Dummy Flask server για να περνάει το health check
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 🔊 Discord Bot Setup
discord.VoiceClient = None  # Disable voice support

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot connected as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# 🧠 Εκκίνηση Flask + Discord Bot
keep_alive()
bot.run(os.environ["TOKEN"])
