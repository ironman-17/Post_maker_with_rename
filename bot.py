import logging
import sys
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL_ID, POST_CHANNELS, TIMEZONE
from utils.helpers import get_greeting, handle_photo, post_to_channels, log_to_channel
from datetime import datetime
import pytz

# Setup logging to stdout
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Commands
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    buttons = ReplyKeyboardMarkup(
        [
            [KeyboardButton("/start"), KeyboardButton("/post")],
            [KeyboardButton("/rename"), KeyboardButton("/status")],
            [KeyboardButton("/log")]
        ],
        resize_keyboard=True
    )
    await message.reply(get_greeting(), reply_markup=buttons)

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

@app.on_message(filters.photo | filters.document | filters.video | filters.audio | filters.sticker | filters.text)
async def handle_message(client, message: Message):
    await post_to_channels(client, message)
    await log_to_channel(client, f"Posted message from {message.from_user.username}: {message.text}")

async def periodic_tasks():
    while True:
        now = datetime.now(pytz.timezone(TIMEZONE))
        if now.hour == 9 and now.minute == 0:
            await app.send_message(LOG_CHANNEL_ID, "Good morning message")
        if now.hour == 21 and now.minute == 0:
            await app.send_message(LOG_CHANNEL_ID, "Good night message")
        await asyncio.sleep(60)

async def main():
    await app.start()
    await periodic_tasks()

if __name__ == "__main__":
    try:
        app.run(main())
    except Exception as e:
        logger.error(f"An error occurred: {e}")
