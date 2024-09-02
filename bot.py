# bot.py

import logging
import asyncio
from datetime import datetime
from pytz import timezone
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI, LOG_CHANNEL_ID, POST_CHANNELS, TIMEZONE
from utils.helpers import get_greeting, handle_photo, post_to_channels, log_to_channel

# Ensure the logs directory exists
import os
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
logging.basicConfig(level=logging.INFO, filename='logs/bot.log', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    await message.reply(get_greeting())

@app.on_message(filters.command("post") & filters.private)
async def post_command(client, message: Message):
    text = message.text.split(None, 1)[1] if len(message.text.split(None, 1)) > 1 else ''
    await post_to_channels(client, text)
    await message.reply("Posted to all channels.")

@app.on_message(filters.command("rename") & filters.private)
async def rename_command(client, message: Message):
    # Implement file renaming logic here
    pass

@app.on_message(filters.command("status") & filters.private)
async def status_command(client, message: Message):
    await message.reply("Bot is running smoothly.")

@app.on_message(filters.command("log") & filters.private)
async def log_command(client, message: Message):
    log_message = "Bot log: " + get_greeting()
    await log_to_channel(client, log_message)
    await message.reply("Logged to the channel.")

async def periodic_tasks():
    while True:
        now = datetime.now(timezone(TIMEZONE))
        if now.hour == 9 and now.minute == 0:
            await app.send_message(LOG_CHANNEL_ID, "Good morning message")
        if now.hour == 21 and now.minute == 0:
            await app.send_message(LOG_CHANNEL_ID, "Good night message")
        await asyncio.sleep(60)

@app.on_message(filters.private)
async def handle_all_messages(client, message: Message):
    await handle_photo(client, message)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(periodic_tasks())
    app.run()  # You can use this in place of loop.run_until_complete(periodic_tasks())
