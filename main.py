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


# ==========================
# 🔁 BATTLE PREVIEW MODULE
# ==========================

class BattleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Attack", emoji="⚔️", style=discord.ButtonStyle.secondary, custom_id="battle_attack")
    async def attack(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You attacked!", ephemeral=True)

    @discord.ui.button(label="Skill 1", emoji="🔥", style=discord.ButtonStyle.danger, custom_id="battle_skill1")
    async def skill1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Skill 1 used!", ephemeral=True)

    @discord.ui.button(label="Skill 2", emoji="🔥", style=discord.ButtonStyle.danger, custom_id="battle_skill2")
    async def skill2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Skill 2 used!", ephemeral=True)

    @discord.ui.button(label="Run", emoji="🏃", style=discord.ButtonStyle.secondary, custom_id="battle_run")
    async def run(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You tried to run!", ephemeral=True)

    @discord.ui.button(label="Change Stance", emoji="🔁", style=discord.ButtonStyle.gray, custom_id="battle_stance")
    async def change_stance(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Stance changed!", ephemeral=True)


def generate_bar(current, max_, color_emoji, size=16):
    filled = round(size * current / max_)
    empty = size - filled
    return color_emoji * filled + "⬛" * empty

def get_hp_mp_display(hp, hp_max, mp, mp_max):
    hp_bar = generate_bar(hp, hp_max, "🟥")
    mp_bar = generate_bar(mp, mp_max, "🟦")
    return f"`{hp}/{hp_max} HP`\n{hp_bar}\n`{mp}/{mp_max} MP`\n{mp_bar}"


@bot.command()
async def testbattle(ctx):
    banner_url = "https://i.imgur.com/K0Q8r3H.jpg"  # μπορείς να το αλλάξεις
    mob_profile_url = "https://i.imgur.com/kc6hY5v.jpg"

    embed = discord.Embed(
        title="🎯 Current Stance: Pinpoint Burst",
        description="Wild Grendel attacked for 26 damage",
        color=discord.Color.dark_gray()
    )

    embed.set_image(url=banner_url)
    embed.set_thumbnail(url=mob_profile_url)

    embed.add_field(
        name="olive",
        value=get_hp_mp_display(142, 180, 55, 90),
        inline=True
    )

    embed.add_field(
        name="Wild Grendel",
        value=get_hp_mp_display(78, 120, 22, 30),
        inline=True
    )

    await ctx.send(embed=embed, view=BattleView())


# 🧠 Εκκίνηση Flask + Discord Bot
keep_alive()
bot.run(os.environ["TOKEN"])
