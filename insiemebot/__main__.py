import asyncio
import discord
import logging
import pytz

from datetime import datetime

import insiemebot.fk as fk
import insiemebot.unicafe as unicafe

from insiemebot.config import Config


client = discord.Client()
cfg = Config()

logging.getLogger().setLevel(logging.INFO)

@client.event
async def on_ready():
    print("Logged in as {}".format(client.user.name))
    print("- - - - - - - - - - - - - - -")
    for guild in client.guilds:
        print("{} - {}".format(guild.name, guild.id))
        for channel in guild.channels:
            print("\t{} - {}".format(channel.name, channel.id))


@client.event
async def on_message(message):
    if message.content == 'unicafe?':
        logging.info("received unicafe?")
        await print_unicafe(message.channel)
    elif message.content == 'fk?':
        logging.info("received fk?")
        await print_fk(message.channel)
    elif message.content == 'fkw?':
        logging.info("received fkw?")
        await print_fkw(message.channel)


async def print_unicafe(channel):
    try:
        msg = "**Unicafe Tagesmenü**\n{}".format(unicafe.today())
    except Exception as e:
        logging.exception("print_unicafe")
        msg = "Error: {}: {}".format(type(e).__name__, e)

    await channel.send(msg)


async def print_fk(channel):
    try:
        msg = "**Froschkönig Menü**\n{}".format(fk.today())
    except Exception as e:
        logging.exception("print_fk")
        msg = "Error: {}: {}".format(type(e).__name__, e)

    await channel.send(msg)


async def print_fkw(channel):
    try:
        menu = fk.get_menu()
    except Exception as e:
        logging.exception("print_fkw")
        msg = "Error: {}: {}".format(type(e).__name__, e)
        await channel.send(msg)
    else:
        await channel.send("**Froschkönig Menü**")
        for (i,m) in enumerate(menu):
            msg = "{}\n{}".format(fk.get_weekdays()[i], m)
            await channel.send(msg)


async def print_fk_periodic():
    while True:
        utcnow = datetime.utcnow().replace(tzinfo=pytz.utc)
        now = utcnow.astimezone(pytz.timezone('Europe/Vienna'))

        if now.minute == 0 and now.hour == 11 and now.weekday() < 5:
            logging.info("GONG")
            channel = client.get_channel(int(cfg['channel']))
            if channel:
                await print_fk(channel)

        await asyncio.sleep(60)


if cfg['token']:
    client.loop.create_task(print_fk_periodic())
    client.run(cfg['token'])
else:
    logging.error('No token present in %s', cfg.config_file)
