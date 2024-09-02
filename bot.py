import logging
import sys
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL_ID, POST_CHANNELS, TIMEZONE
from datetime import datetime
import pytz

# Setup logging to stdout
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Helper functions
def get_greeting():
    now = datetime.now(pytz.timezone('Asia/Kolkata'))
    hour = now.hour
    if 5 <= hour < 12:
        return "Good morning!"
    elif 12 <= hour < 17:
        return "Good afternoon!"
    elif 17 <= hour < 21:
        return "Good evening!"
    else:
        return "Good night!"

async def post_to_channels(client: Client, message: Message):
    for channel in POST_CHANNELS:
        try:
            if message.photo:
                await client.send_photo(
                    chat_id=channel,
                    photo=message.photo.file_id,
                    caption=message.caption or "Here is the photo!"  # Optional caption
                )
            elif message.document:
                await client.send_document(
                    chat_id=channel,
                    document=message.document.file_id,
                    caption=message.caption or "Here is the document!"  # Optional caption
                )
            elif message.video:
                await client.send_video(
                    chat_id=channel,
                    video=message.video.file_id,
                    caption=message.caption or "Here is the video!"  # Optional caption
                )
            elif message.audio:
                await client.send_audio(
                    chat_id=channel,
                    audio=message.audio.file_id,
                    caption=message.caption or "Here is the audio!"  # Optional caption
                )
            elif message.sticker:
                await client.send_sticker(
                    chat_id=channel,
                    sticker=message.sticker.file_id
                )
            else:
                await client.send_message(channel, message.text)
        except Exception as e:
            print(f"Error sending message to {channel}: {e}")

async def log_to_channel(client: Client, message: str):
    try:
        await client.send_message(LOG_CHANNEL_ID, message)
    except Exception as e:
        print(f"Error logging message: {e}")

async def handle_photo(client: Client, message: Message):
    if message.photo:
        caption = "Auto-captioned text here"
        try:
            await client.send_photo(
                chat_id=message.chat.id,
                photo=message.photo.file_id,
                caption=caption
            )
        except Exception as e:
            print(f"Error sending photo caption: {e}")

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
    if message.reply_to_message:
        reply_message = message.reply_to_message
        try:
            if reply_message.text or reply_message.photo or reply_message.document or reply_message.video or reply_message.audio or reply_message.sticker:
                await post_to_channels(client, reply_message)
                await message.reply("Posted to all channels.")
            else:
                await message.reply("Reply message type not supported for posting.")
        except Exception as e:
            await message.reply(f"An error occurred: {e}")
    else:
        await message.reply("Please reply to a message you want to post.")

@app.on_message(filters.command("rename") & filters.private)
async def rename_command(client, message: Message):
    if message.reply_to_message:
        reply_message = message.reply_to_message
        try:
            new_file_name = "new_name_here"  # Replace with actual logic to get the new file name
            await rename_file(client, reply_message, new_file_name)
            await message.reply("File renamed successfully.")
        except Exception as e:
            await message.reply(f"An error occurred: {e}")
    else:
        await message.reply("Please reply to a message containing a file you want to rename.")

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
    logger.info("Bot has started.")
    await app.send_message(LOG_CHANNEL_ID, "Bot has started.")
    await periodic_tasks()

if __name__ == "__main__":
    try:
        app.run(main())
    except Exception as e:
        logger.error(f"An error occurred: {e}")
