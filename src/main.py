# https://discord.com/oauth2/authorize?client_id=875157389626716170&scope=bot&permissions=8589934591

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


bot = commands.Bot(command_prefix="$")

@bot.event
async def on_ready():
    bot_channel = bot.get_channel(875147778882412604)
    await bot_channel.send("Online.")

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.command()
async def dm(message):
    await message.author.send("Alright. Here is your direct message.")

load_dotenv()
bot.run(os.getenv('TOKEN'))
