from pyrogram import Client, filters
from pyrogram.types import Message
from config import POST_CHANNELS, LOG_CHANNEL_ID
from datetime import datetime
from pytz import timezone

# Function to post string/text directly to channels
async def post_text_to_channels(client: Client, text: str):
    try:
        # Agar text string hai, toh post karo sabhi channels mein
        for channel in POST_CHANNELS:
            await client.send_message(
                chat_id=channel,
                text=text  # Send direct text to the channel
            )
    except Exception as e:
        print(f"Error sending message to {channel}: {e}")

# Function to post media to channels
async def post_media_to_channels(client: Client, message: Message):
    try:
        # Media check (no text handling here)
        if message.photo:  # Agar message photo ho
            for channel in POST_CHANNELS:
                await client.send_photo(
                    chat_id=channel,
                    photo=message.photo.file_id,
                    caption=message.caption or "Here is a photo!"
                )

        elif message.document:  # Agar message document ho
            for channel in POST_CHANNELS:
                await client.send_document(
                    chat_id=channel,
                    document=message.document.file_id,
                    caption=message.caption or "Here is a document!"
                )

        elif message.video:  # Agar message video ho
            for channel in POST_CHANNELS:
                await client.send_video(
                    chat_id=channel,
                    video=message.video.file_id,
                    caption=message.caption or "Here is a video!"
                )

        elif message.audio:  # Agar message audio ho
            for channel in POST_CHANNELS:
                await client.send_audio(
                    chat_id=channel,
                    audio=message.audio.file_id,
                    caption=message.caption or "Here is an audio!"
                )

        elif message.sticker:  # Agar message sticker ho
            for channel in POST_CHANNELS:
                await client.send_sticker(
                    chat_id=channel,
                    sticker=message.sticker.file_id
                )

        else:
            print(f"Message type not supported: {message}")

    except Exception as e:
        print(f"Error sending message to {channel}: {e}")

# Error handling function to log any issues
async def log_to_channel(client: Client, message: str):
    try:
        await client.send_message(LOG_CHANNEL_ID, message)
    except Exception as e:
        print(f"Error logging message: {e}")

# Handler for string/text messages
@Client.on_message(filters.text)
async def handle_text(client: Client, message: Message):
    if isinstance(message.text, str):
        try:
            await post_text_to_channels(client, message.text)
        except Exception as e:
            print(f"Error occurred while handling text: {e}")

# Handler for media messages (photo, document, video, audio, sticker)
@Client.on_message(filters.photo | filters.document | filters.video | filters.audio | filters.sticker)
async def handle_media(client: Client, message: Message):
    try:
        await post_media_to_channels(client, message)
    except Exception as e:
        print(f"Error occurred while handling media: {e}")

# Greeting function (Optional, can be used elsewhere if needed)
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
