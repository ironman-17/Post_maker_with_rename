from pyrogram import Client
from pyrogram.types import Message

async def post_to_channels(client: Client, message: Message):
    # Ensure the message is a proper Pyrogram Message object before processing
    if isinstance(message, Message):
        for channel in POST_CHANNELS:
            try:
                # Handle media types
                if message.photo:
                    await client.send_photo(
                        chat_id=channel,
                        photo=message.photo.file_id,
                        caption=message.caption or "Here is the photo!"
                    )
                elif message.document:
                    await client.send_document(
                        chat_id=channel,
                        document=message.document.file_id,
                        caption=message.caption or "Here is the document!"
                    )
                elif message.video:
                    await client.send_video(
                        chat_id=channel,
                        video=message.video.file_id,
                        caption=message.caption or "Here is the video!"
                    )
                elif message.audio:
                    await client.send_audio(
                        chat_id=channel,
                        audio=message.audio.file_id,
                        caption=message.caption or "Here is the audio!"
                    )
                elif message.sticker:
                    await client.send_sticker(
                        chat_id=channel,
                        sticker=message.sticker.file_id
                    )
                elif message.text:
                    await client.send_message(
                        chat_id=channel,
                        text=message.text
                    )
            except Exception as e:
                print(f"Error sending message to {channel}: {e}")
    else:
        print("Error: The provided message is not a valid Pyrogram Message object.")
