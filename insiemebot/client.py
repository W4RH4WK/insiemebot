import asyncio
import discord
import pytz
import logging

from datetime import datetime
from insiemebot.fk import today


DEFAULT_CHANNEL = '339391485692608512'


client = discord.Client()


@client.event
async def on_ready():
    print("Logged in as {}".format(client.user.name))
    print("- - - - - - - - - - - - - - -")
    for server in client.servers:
        print("{} - {}".format(server.name, server.id))
        for channel in server.channels:
            print("\t{} - {}".format(channel.name, channel.id))

    asyncio.ensure_future(print_fk_periodic())


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
            await print_fk(client.get_channel(DEFAULT_CHANNEL))

        await asyncio.sleep(60)
