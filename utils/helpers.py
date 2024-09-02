from datetime import datetime
from pytz import timezone
from pyrogram import Client
from pyrogram.types import Message  # Correct import for Message
from config import POST_CHANNELS, LOG_CHANNEL_ID  # Ensure these are imported

def get_greeting():
    now = datetime.now(timezone('Asia/Kolkata'))
    hour = now.hour
    if 5 <= hour < 12:
        return "Good morning!"
    elif 12 <= hour < 17:
        return "Good afternoon!"
    elif 17 <= hour < 21:
        return "Good evening!"
    else:
        return "Good night!"

async def post_to_channels(client: Client, text: str):
    for channel in POST_CHANNELS:
        await client.send_message(channel, text)

async def log_to_channel(client: Client, message: str):
    await client.send_message(LOG_CHANNEL_ID, message)

async def handle_photo(client: Client, message: Message):
    if message.photo:
        # Implement photo auto-captioning logic here
        caption = "Auto-captioned text here"
        await client.send_message(message.chat.id, caption)
