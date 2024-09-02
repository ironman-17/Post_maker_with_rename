import logging
import sys
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL_ID, POST_CHANNELS, TIMEZONE
from utils.helpers import get_greeting, handle_photo, post_to_channels, log_to_channel
from datetime import datetime, timedelta
import pytz

# Setup logging to stdout
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# State management
user_state = {}

# Commands
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    user_id = message.from_user.id
    user_state[user_id] = None  # Clear any active state
    buttons = ReplyKeyboardMarkup(
        [
            [KeyboardButton("/start"), KeyboardButton("/post")],
            [KeyboardButton("/rename"), KeyboardButton("/status")],
            [KeyboardButton("/log"), KeyboardButton("Schedule Post")]
        ],
        resize_keyboard=True
    )
    await message.reply(get_greeting(), reply_markup=buttons)

@app.on_message(filters.command("post") & filters.private)
async def post_command(client, message: Message):
    user_id = message.from_user.id
    user_state[user_id] = 'post'  # Set state to 'post'
    await message.reply("Please send the text or media you want to post.")

@app.on_message(filters.text & filters.private)
async def handle_text(client, message: Message):
    user_id = message.from_user.id
    if message.text == "Schedule Post":
        user_state[user_id] = 'schedule'  # Set state to 'schedule'
        await message.reply("Please send the text you want to schedule.")
    elif user_state.get(user_id) == 'post':
        text = message.text
        await post_to_channels(client, text)
        await message.reply("Posted to all channels.")
        user_state[user_id] = None  # Clear the state after posting
    elif user_state.get(user_id) == 'schedule':
        user_state[user_id] = 'schedule_text'
        user_state[user_id] = {'schedule_message': message.text}
        await message.reply("Please enter the time to post (HH:MM format):")
    elif user_state.get(user_id) == 'schedule_text':
        try:
            schedule_time = datetime.strptime(message.text, "%H:%M").time()
            now = datetime.now(pytz.timezone(TIMEZONE))
            scheduled_datetime = datetime.combine(now.date(), schedule_time)
            if scheduled_datetime < now:
                scheduled_datetime += timedelta(days=1)
            delay = (scheduled_datetime - now).total_seconds()
            await asyncio.create_task(schedule_post(client, user_state[user_id]['schedule_message'], delay))
            await message.reply(f"Message scheduled for {scheduled_datetime.strftime('%H:%M')}.")
            user_state[user_id] = None  # Clear the state after scheduling
        except ValueError:
            await message.reply("Invalid time format. Please enter the time as HH:MM.")
            user_state[user_id] = 'schedule_text'  # Prompt to re-enter time

async def schedule_post(client, text, delay):
    await asyncio.sleep(delay)
    await post_to_channels(client, text)

@app.on_message(filters.command("rename") & filters.private)
async def rename_command(client, message: Message):
    user_id = message.from_user.id
    user_state[user_id] = 'rename'  # Set state to 'rename'
    await message.reply("Please send the file you want to rename.")

@app.on_message(filters.media & filters.private)
async def handle_media(client, message: Message):
    user_id = message.from_user.id
    if user_state.get(user_id) == 'rename':
        # Implement the file renaming logic here
        await message.reply("File has been renamed.")
        user_state[user_id] = None  # Clear the state after renaming
    elif user_state.get(user_id) == 'post':
        await post_to_channels(client, message)
        await message.reply("Posted to all channels.")
        user_state[user_id] = None  # Clear the state after posting

@app.on_message(filters.command("status") & filters.private)
async def status_command(client, message: Message):
    user_id = message.from_user.id
    user_state[user_id] = None  # Clear any active state
    await message.reply("Bot is running smoothly.")

@app.on_message(filters.command("log") & filters.private)
async def log_command(client, message: Message):
    user_id = message.from_user.id
    user_state[user_id] = None  # Clear any active state
    log_message = "Bot log: " + get_greeting()
    await log_to_channel(client, log_message)
    await message.reply("Logged to the channel.")

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
