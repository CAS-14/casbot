import os
from discord import *
from discord.ext import commands
import cogs.cb_util as util
from firebase_admin import db

TOKEN = os.getenv('DISCORD_TOKEN')

# activity = Game(name=gameStatus)
# activity = Streaming(name="c!help", url="twitch_url_here")
# activity = Activity(type=ActivityType.listening, name="!help")
# activity = Activity(type=ActivityType.watching, name="!help")

bot = commands.Bot(command_prefix=util.prefix, status=Status.online)

verbose_start = False

"""
@bot.event
async def on_message(message):
    await message.reply("i'm dad") if message.author.id != bot.user.id else None
    await bot.process_commands(message)
"""

@bot.event
async def on_ready():
    bt_channel = bot.get_channel(util.channel_ids['BT-casbot']) 

    online_msg = await bt_channel.send(':cold_face: CASbot is online!')

    release_ver = -1
    try:
        ref = db.reference("/bot-data/release-ver/")
        release_ver = int(ref.get()) + 1
        ref.set(release_ver)
        await online_msg.edit(content = online_msg.content + " `[rv " + str(release_ver) + "]`")
    except Exception as e:
        release_ver = None
        await online_msg.edit(content = online_msg.content + f"\n:warning:{e}")

    for ext in util.cog_exts:
        try:
            bot.load_extension('cogs.cog_'+ext)
            await online_msg.edit(content = online_msg.content + f'\n:white_check_mark: Cog extension `{ext}` loaded successfully!') if verbose_start else None
        except Exception as e:
            await online_msg.edit(content = online_msg.content + f'\n:warning: Could not load cog extension `{ext}`.\n```\n{e}\n```')
            await bot.change_presence(activity=Game(name=f"cog error for {ext}..."))

bot.run(TOKEN)
