import discord
import os
from discord.ext import commands
import asyncio
import json

sec_token = os.environ['DISCORD_TOKEN']
sec_channel = os.environ['CHANNEL_ID']
snippets_path = "snippets.json"
state_path = "state.json"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='<', intents=intents)
channel = bot.get_channel(int(sec_channel))
initial_state = {"current_index": 0}


def load_snippets():
    with open(snippets_path, "r") as f:
        return json.load(f)


def load_state():
    with open(state_path, "r") as f:
        return json.load(f)


def save_state(current_index):
    with open("state.json", "w") as f:
        json.dump({"current_index": current_index}, f)


async def send_snippet():
    while True:
        state = load_state()
        current_index = state["current_index"]

        snippets = load_snippets()

        if current_index >= len(snippets):
            current_index = 0

        snippet = snippets[current_index]

        channel = bot.get_channel(int(sec_channel))

        message = f"**{snippet['title']}**\n{snippet['code']}"

        await channel.send(message)

        current_index += 1
        save_state(current_index)

        await asyncio.sleep(86400)


@bot.command()
async def reset_index(ctx):
    global current_index
    current_index = 0
    save_state(current_index)
    await ctx.send("Index wurde auf 0 zurückgesetzt.")


@bot.event
async def on_ready():
    print(f'Bot is logged in as {bot.user}')
    bot.loop.create_task(send_snippet())


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


bot.run(sec_token)
