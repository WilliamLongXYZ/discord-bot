# https://discord.com/oauth2/authorize?client_id=875157389626716170&scope=bot&permissions=8589934591

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


bot = commands.Bot(command_prefix="$", help_command=None)

@bot.event
async def on_ready():
    bot_channel = bot.get_channel(875147778882412604)
    await bot.change_presence(status=discord.Status.online)
    await bot.change_presence(activity=discord.Game(name="FLOSS Simulator"))
    await bot_channel.send("Online.")

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.command()
async def dm(message):
    await message.author.send("Alright. Here is your direct message.")

@bot.command()
async def echo(ctx, *, arg):
    await ctx.send(arg)

@bot.command(pass_context=True)
async def purge(ctx, amnt=5):
    await ctx.channel.purge(limit=amnt)

@bot.command()
async def source(ctx):
    await ctx.send("https://github.com/xarvveron/discord-bot")

@bot.group(name="help", invoke_without_command=True)
async def help(ctx):
    help_embed = discord.Embed(title="Help", description="Use $help <command> for extended information.")
    help_embed.add_field(name="General", value="help, source")
    help_embed.add_field(name="Moderation", value="purge")

    await ctx.send(embed=help_embed)

@help.command(name="general")
async def general(ctx):
    general_embed = discord.Embed(title="General Commands", description="Use $help <command for extended information.")
    general_embed.add_field(name="help", value="Show information on all available commands.")
    general_embed.add_field(name="source", value="Show a link to the source code of this bot.")
    
    await ctx.send(embed=general_embed)

@help.command(name="moderation")
async def moderation(ctx):
    moderation_embed = discord.Embed(title="Moderation Commands", description="Use $help <command> for extended information.")
    moderation_embed.add_field(name="Purge", value="Clear messages from the channel you use this is.")

    await ctx.send(embed=moderation_embed)

load_dotenv()
bot.run(os.getenv('TOKEN'))
