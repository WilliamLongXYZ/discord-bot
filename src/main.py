# https://discord.com/oauth2/authorize?client_id=875157389626716170&scope=bot&permissions=8589934591

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import nacl.utils

import youtube_dl

prefix = '$'
bot = commands.Bot(command_prefix=prefix, help_command=None)

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
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'User {member} has been banned.')

@bot.command()
async def dm(message):
    await message.author.send("Alright. Here is your direct message.")

@bot.command()
async def echo(ctx, *, arg):
    await ctx.send(arg)













@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")






ytdl = youtube_dl.YoutubeDL()
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

@bot.command(name='play')
async def play(ctx, url):
    filename = await YTDLSource.from_url(url, loop=bot.loop)
    ctx.message.guild.voice_client.play(discord.FFmpegPCMAudio(executable="E:/ffmpeg/bin/ffmpeg.exe", source=filename))
    await ctx.send(f'Playing: {filename}')



@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been kicked.')

@bot.command()
async def purge(ctx, amnt=5):
    await ctx.channel.purge(limit=amnt)

@bot.command()
async def source(ctx):
    await ctx.send("https://github.com/xarvveron/discord-bot")

@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'User {member} has been unbanned.')
            return

@bot.group(name="channel", invoke_without_command=True)
async def channel(ctx):
    await ctx.send(f'Use `{prefix}help channel` for more usage information.')

@channel.command(name="create")
async def create(ctx, name):
    await ctx.guild.create_text_channel(name)
    for channel in ctx.guild.channels:
        if channel.name == name:
            id = channel.id
    await ctx.send(f'The channel <#{id}> has been created.')

@channel.command(name="delete")
async def delete(ctx, channel: discord.TextChannel):
    await channel.delete()

@channel.command(name="list")
async def list(ctx):
    channels = ctx.guild.text_channels
    channel_str = ''
    for channel in channels:
        channel_str += str(channel)+'\n'
    await ctx.send(channel_str)

@channel.command(name="purge")
async def purge(ctx):
    for channel in ctx.guild.channels:
        await channel.delete()

@channel.command(name="query")
async def query(ctx):
    channels = bot.get_all_channels()
    channel_str = ''
    for channel in channels:
        channel_str += str(channel)+'\n'
    await ctx.send(channel_str)

@channel.command(name="textpurge")
async def textpurge(ctx):
    for channel in ctx.guild.text_channels:
        await channel.delete()

@channel.command(name="wipe")
async def wipe(ctx, name):
    for channel in ctx.guild.channels:
        if channel.name == name:
            await channel.delete()

@bot.group(name="voice", invoke_without_command=True)
async def voice(ctx):
    await ctx.send(f'Use `{prefix}help voice` for more usage information.')

@voice.group(name="create")
async def create(ctx, name):
    await ctx.guild.create_voice_channel(name)
    for channel in ctx.guild.channels:
        if channel.name == name:
            id = channel.id
    await ctx.send(f'The channel <#{id}> has been created.')

@voice.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()



@voice.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.group(name="help", invoke_without_command=True)
async def help(ctx):
    help_embed = discord.Embed(title="Help", description="Use $help <command> for extended information.")
    help_embed.add_field(name="General", value="dm, echo, help, source, voice")
    help_embed.add_field(name="Moderation", value="ban, channel, kick, purge, unban")

    await ctx.send(embed=help_embed)

@help.command(name="general")
async def general(ctx):
    general_embed = discord.Embed(title="General Commands", description="Use $help <command for extended information.")
    general_embed.add_field(name="dm", value="Receive a direct message from this bot.")
    general_embed.add_field(name="echo", value="Repeat what the user inputs.")
    general_embed.add_field(name="help", value="Show information on all available commands.")
    general_embed.add_field(name="source", value="Show a link to the source code of this bot.")
    general_embed.add_field(name="voice", value="A collection of sub-commands to create, join, leave, and handle voice channels")
    
    await ctx.send(embed=general_embed)

@help.command(name="moderation")
async def moderation(ctx):
    moderation_embed = discord.Embed(title="Moderation Commands", description="Use $help <command> for extended information.")
    moderation_embed.add_field(name="ban", value="Ban a user from the server.")
    moderation_embed.add_field(name="channel", value="A collection of sub-commands to handle creation and editing of channels.")
    moderation_embed.add_field(name="kick", value="Kick a user from the server.")
    moderation_embed.add_field(name="purge", value="Clear messages from the channel you use this is.")
    moderation_embed.add_field(name="unban", value="Unban a user from the server.")

    await ctx.send(embed=moderation_embed)

load_dotenv()
bot.run(os.getenv('TOKEN'))
