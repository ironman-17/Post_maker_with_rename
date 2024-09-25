import logging
import sys
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL_ID, POST_CHANNELS, TIMEZONE, OWNER_ID
from utils.helpers import get_greeting, handle_photo, post_to_channels, log_to_channel
from datetime import datetime, timedelta
import pytz

# Setup logging to stdout
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# State management
user_state = {}

async def is_owner(user_id):
    return user_id == OWNER_ID

# Commands
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    user_id = message.from_user.id
    logger.info(f"/start command received from {user_id}")
    
    if not await is_owner(user_id):
        await message.reply("You are not authorized to use this bot.")
        logger.warning(f"Unauthorized user {user_id} tried to use /start")
        return
    
    user_state[user_id] = None  # Clear any active state
    buttons = ReplyKeyboardMarkup(
        [
            [KeyboardButton("/start"), KeyboardButton("/post")],
            [KeyboardButton("/rename"), KeyboardButton("/status")],
            [KeyboardButton("/log"), KeyboardButton("/schedule")]
        ],
        resize_keyboard=True
    )
    await message.reply(get_greeting(), reply_markup=buttons)
    logger.info(f"Reply sent to {user_id} with menu buttons")

@app.on_message(filters.command("post") & filters.private)
async def post_command(client, message: Message):
    user_id = message.from_user.id
    logger.info(f"/post command received from {user_id}")
    
    if not await is_owner(user_id):
        await message.reply("You are not authorized to use this bot.")
        logger.warning(f"Unauthorized user {user_id} tried to use /post")
        return
    
    user_state[user_id] = 'post'  # Set state to 'post'
    await message.reply("Please send the text or media you want to post.")
    logger.info(f"User {user_id} is now in 'post' state")

@app.on_message(filters.command("schedule") & filters.private)
async def schedule_command(client, message: Message):
    user_id = message.from_user.id
    logger.info(f"/schedule command received from {user_id}")
    
    if not await is_owner(user_id):
        await message.reply("You are not authorized to use this bot.")
        logger.warning(f"Unauthorized user {user_id} tried to use /schedule")
        return
    
    user_state[user_id] = 'schedule'  # Set state to 'schedule'
    await message.reply("Please send the text or media you want to schedule.")
    logger.info(f"User {user_id} is now in 'schedule' state")

@app.on_message(filters.text & filters.private)
async def handle_text(client, message: Message):
    user_id = message.from_user.id
    state = user_state.get(user_id)
    
    if state == 'post':
        text = message.text
        await post_to_channels(client, text)
        await message.reply("Posted to all channels.")
        user_state[user_id] = None  # Clear the state after posting
        logger.info(f"Message posted by {user_id}: {text}")
    elif state == 'schedule':
        user_state[user_id] = 'schedule_text'
        user_state['schedule_message'] = message.text
        await message.reply("Please enter the time to post (HH:MM format):")
        logger.info(f"Scheduling message received from {user_id}")
    elif state == 'schedule_text':
        try:
            schedule_time = datetime.strptime(message.text, "%H:%M").time()
            now = datetime.now(pytz.timezone(TIMEZONE))
            scheduled_datetime = datetime.combine(now.date(), schedule_time)
            scheduled_datetime = pytz.timezone(TIMEZONE).localize(scheduled_datetime)

            if scheduled_datetime < now:
                scheduled_datetime += timedelta(days=1)
            delay = (scheduled_datetime - now).total_seconds()
            asyncio.create_task(schedule_post(client, user_state['schedule_message'], delay))
            await message.reply(f"Message scheduled for {schedule_time}.")
            user_state[user_id] = None
            logger.info(f"Message scheduled by {user_id} for {schedule_time}")
        except ValueError:
            await message.reply("Invalid time format. Please enter the time as HH:MM.")
            logger.error(f"Invalid time format entered by {user_id}: {message.text}")

@app.on_message(filters.media & filters.private)
async def handle_media(client, message: Message):
    user_id = message.from_user.id
    state = user_state.get(user_id)
    
    if state == 'rename':
        # Implement the file renaming logic here
        await message.reply("File has been renamed.")
        user_state[user_id] = None  # Clear the state after renaming
        logger.info(f"File renamed for {user_id}")
    elif state == 'post':
        await post_to_channels(client, message)
        await message.reply("Posted to all channels.")
        user_state[user_id] = None  # Clear the state after posting
        logger.info(f"Media posted by {user_id}")
    elif state == 'schedule':
        user_state['schedule_message'] = message
        await message.reply("Please enter the time to post (HH:MM format):")
        user_state[user_id] = 'schedule_text'
        logger.info(f"Media received for scheduling from {user_id}")

@app.on_message(filters.command("rename") & filters.private)
async def rename_command(client, message: Message):
    user_id = message.from_user.id
    logger.info(f"/rename command received from {user_id}")
    
    if not await is_owner(user_id):
        await message.reply("You are not authorized to use this bot.")
        logger.warning(f"Unauthorized user {user_id} tried to use /rename")
        return
    
    user_state[user_id] = 'rename'  # Set state to 'rename'
    await message.reply("Please send the file you want to rename.")

@app.on_message(filters.command("status") & filters.private)
async def status_command(client, message: Message):
    user_id = message.from_user.id
    logger.info(f"/status command received from {user_id}")
    
    if not await is_owner(user_id):
        await message.reply("You are not authorized to use this bot.")
        return
    
    await message.reply("Bot is running smoothly.")
    logger.info(f"Status request handled for {user_id}")

@app.on_message(filters.command("log") & filters.private)
async def log_command(client, message: Message):
    user_id = message.from_user.id
    logger.info(f"/log command received from {user_id}")
    
    if not await is_owner(user_id):
        await message.reply("You are not authorized to use this bot.")
        return
    
    log_message = "Bot log: " + get_greeting()
    await log_to_channel(client, log_message)
    await message.reply("Logged to the channel.")
    logger.info(f"Log sent to channel by {user_id}")

async def schedule_post(client, message, delay):
    await asyncio.sleep(delay)
    await post_to_channels(client, message)
    logger.info("Scheduled post sent.")

async def periodic_tasks():
    while True:
        now = datetime.now(pytz.timezone(TIMEZONE))
        if now.hour == 9 and now.minute == 0:
            await app.send_message(LOG_CHANNEL_ID, "Good morning Sir")
        if now.hour == 21 and now.minute == 0:
            await app.send_message(LOG_CHANNEL_ID, "Good night Sir")
        await asyncio.sleep(60)

async def main():
    await app.start()
    await periodic_tasks()

if __name__ == "__main__":
    try:
        app.run(main())
    except Exception as e:
        logger.error(f"An error occurred: {e}")
