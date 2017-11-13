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


@client.event
async def on_ready():
    print("Logged in as {}".format(client.user.name))
    print("- - - - - - - - - - - - - - -")
    for server in client.servers:
        print("{} - {}".format(server.name, server.id))
        for channel in server.channels:
            print("\t{} - {}".format(channel.name, channel.id))


@client.event
async def on_message(message):
    if message.content == 'unicafe?':
        logging.info("received unicafe?")
        await print_unicafe(message.channel)
    if message.content == 'fk?':
        logging.info("received fk?")
        await print_fk(message.channel)
    if message.content == 'fkw?':
        logging.info("received fkw?")
        await print_fkw(message.channel)

async def print_unicafe(channel):
    try:
        msg = "**Unicafe Tagesmenü**\n{}".format(unicafe.today())
    except Exception as e:
        logging.exception("print_unicafe")
        msg = "Error: {}: {}".format(type(e).__name__, e)

    await client.send_message(channel, msg)

async def print_fk(channel):
    try:
        msg = "**Froschkönig Menü**\n{}".format(fk.today())
    except Exception as e:
        logging.exception("print_fk")
        msg = "Error: {}: {}".format(type(e).__name__, e)

    await client.send_message(channel, msg)

async def print_fkw(channel):
    try:
        msg = "**Froschkönig Menü**\n{}".format(fk.this_week())
    except Exception as e:
        logging.exception("print_fkw")
        msg = "Error: {}: {}".format(type(e).__name__, e)

    await client.send_message(channel, msg)

async def print_fk_periodic():
    while True:
        utcnow = datetime.utcnow().replace(tzinfo=pytz.utc)
        now = utcnow.astimezone(pytz.timezone('Europe/Vienna'))

        if now.minute == 0 and now.hour == 11 and now.weekday() < 5:
            logging.info("GONG")
            for server in client.servers:
                await print_fk(server.default_channel)

        await asyncio.sleep(60)


if cfg['token']:
    client.loop.create_task(print_fk_periodic())
    client.run(cfg['token'])
else:
    logging.error('No token present in %s', cfg.config_file)
