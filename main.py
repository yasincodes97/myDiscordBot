import discord
import os
from discord.ext import commands
import asyncio
import sqlite3
import json
from server import stay_alive

sec_token = os.environ['DISCORD_TOKEN']
sec_channel = os.environ['CHANNEL_ID']
snippets_path = "snippets.json"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='<', intents=intents)
#bruder 
def setup_db():
    conn = sqlite3.connect("state.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS bot_state (id INTEGER PRIMARY KEY, current_index INTEGER)")
    c.execute("SELECT COUNT(*) FROM bot_state")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO bot_state (id, current_index) VALUES (1, 0)")
    conn.commit()
    conn.close()

def load_state():
    conn = sqlite3.connect("state.db")
    c = conn.cursor()
    c.execute("SELECT current_index FROM bot_state WHERE id = 1")
    result = c.fetchone()
    conn.close()
    return result[0]

def save_state(current_index):
    conn = sqlite3.connect("state.db")
    c = conn.cursor()
    c.execute("UPDATE bot_state SET current_index = ? WHERE id = 1", (current_index,))
    conn.commit()
    conn.close()

def load_snippets():
    with open(snippets_path, "r") as f:
        return json.load(f)

async def send_snippet():
    while True:
        current_index = load_state()
        snippets = load_snippets()

        if current_index >= len(snippets):
            current_index = 0

        snippet = snippets[current_index]
        channel = bot.get_channel(int(sec_channel))
        message = f"**{snippet['title']}**\n{snippet['code']}"
        await channel.send(message)

        current_index += 1
        save_state(current_index)

        await asyncio.sleep(86400)  # 24h

@bot.command()
async def reset_index(ctx):
    save_state(0)
    await ctx.send("Index wurde auf 0 zurückgesetzt.")

@bot.event
async def on_ready():
    print(f'Bot is logged in as {bot.user}')
    bot.loop.create_task(send_snippet())

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="🤝・vorstellungsrunde")
    if channel:
        await channel.send(f"Welcome to the Tech-Hood family, {member.mention}! 🎉")

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

setup_db()
stay_alive()
bot.run(sec_token)
