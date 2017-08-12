import asyncio
import discord
import pytz
import logging

from datetime import datetime
from insiemebot.config import Config
from insiemebot.fk import today


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
    if message.content == '!fk':
        logging.info("received !fK")
        await print_fk(message.channel)


async def print_fk(channel):
    try:
        msg = "**Froschkönig Menü**\n{}".format(today())
    except Exception as e:
        logging.exception("print_fk")
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
