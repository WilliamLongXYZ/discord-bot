# https://discord.com/oauth2/authorize?client_id=875157389626716170&scope=bot&permissions=8589934591

import os

import discord
from dotenv import load_dotenv


client = discord.Client()

@client.event
async def on_ready():
    bot_channel = client.get_channel(875147778882412604)
    await bot_channel.send("Online.")

load_dotenv()
client.run(os.getenv('TOKEN'))
