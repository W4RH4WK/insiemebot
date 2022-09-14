import asyncio
import discord
import logging
import pytz

from datetime import datetime
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks

from insiemebot import fk
from insiemebot.config import Config


logging.getLogger().setLevel(logging.INFO)
cfg = Config()

if not cfg['token']:
    logging.error('No token present in %s', cfg.config_file)
    sys.exit(1)


class Insiemebot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync(guild=discord.Object(id=cfg['guild']))
        print("Synced slash commands")

    async def on_ready(self):
        print("Logged in as {}".format(self.user.name))
        print("- - - - - - - - - - - - - - -")
        for guild in self.guilds:
            print("{} - {}".format(guild.name, guild.id))
            for channel in guild.channels:
                print("\t{} - {}".format(channel.name, channel.id))

        fk_periodic.start()


bot = Insiemebot()

@bot.hybrid_command(name='fk', with_app_command=True, description='Display Froschkönig menu of today')
@app_commands.guilds(discord.Object(id=cfg['guild']))
async def fk_today(ctx):
    try:
        msg = "**Froschkönig Menü**\n{}".format(fk.today())
    except Exception as e:
        logging.exception("print_fk")
        msg = "Error: {}: {}".format(type(e).__name__, e)
    await ctx.send(msg)

@bot.hybrid_command(name='fkw', with_app_command=True, description='Display Froschkönig menu for the whole week')
@app_commands.guilds(discord.Object(id=cfg['guild']))
async def fk_week(ctx):
    try:
        menu = fk.get_menu()
    except Exception as e:
        logging.exception("print_fkw")
        msg = "Error: {}: {}".format(type(e).__name__, e)
        await ctx.send(msg)
    else:
        await ctx.send("**Froschkönig Menü**")
        for (i,m) in enumerate(menu):
            msg = "{}\n{}".format(fk.get_weekdays()[i], m)
            await ctx.send(msg)

@tasks.loop(minutes=1)
async def fk_periodic():
    utcnow = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = utcnow.astimezone(pytz.timezone('Europe/Vienna'))

    if now.minute == 0 and now.hour == 11 and now.weekday() < 5:
        logging.info("GONG")
        channel = bot.get_channel(int(cfg['channel']))
        if channel:
            await fk_today(channel)
        else:
            logging.error("no such channel")

bot.run(cfg['token'])
