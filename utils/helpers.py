from datetime import datetime
from pytz import timezone
from pyrogram import Client
from pyrogram.types import Message
from config import POST_CHANNELS, LOG_CHANNEL_ID

def get_greeting():
    now = datetime.now(timezone('Asia/Kolkata'))
    hour = now.hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 21:
        return "Good evening"
    else:
        return "Good night"

async def post_to_channels(client: Client, message: Message):
    for channel in POST_CHANNELS:
        try:
            if message.photo:
                # Send photo to channel
                await client.send_photo(
                    chat_id=channel,
                    photo=message.photo.file_id,
                    caption=message.caption or "Here is the photo!"  # Optional caption
                )
            elif message.document:
                # Send document to channel
                await client.send_document(
                    chat_id=channel,
                    document=message.document.file_id,
                    caption=message.caption or "Here is the document!"  # Optional caption
                )
            elif message.video:
                # Send video to channel
                await client.send_video(
                    chat_id=channel,
                    video=message.video.file_id,
                    caption=message.caption or "Here is the video!"  # Optional caption
                )
            elif message.audio:
                # Send audio to channel
                await client.send_audio(
                    chat_id=channel,
                    audio=message.audio.file_id,
                    caption=message.caption or "Here is the audio!"  # Optional caption
                )
            elif message.sticker:
                # Send sticker to channel
                await client.send_sticker(
                    chat_id=channel,
                    sticker=message.sticker.file_id
                )
            elif message.text:
                # Send text to channel
                await client.send_message(
                    chat_id=channel,
                    text=message.text
                )
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
