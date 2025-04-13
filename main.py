import discord
import os
from discord.ext import commands
import AsyncIOScheduler
import datetime


token = os.environ['DISCORD_TOKEN']
sec_token = os.environ['DISCORD_TOKEN']
sec_channel = os.environ['DISCORD_CHANNEL']

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='<', intents=intents)

@bot.command()
async def ping(msg):
    await msg.send('pong')


bot.run(sec_token)