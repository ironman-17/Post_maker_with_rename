from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL_ID, POST_CHANNELS
from helpers import get_greeting, handle_photo, post_to_channels, log_to_channel
from datetime import datetime
import pytz

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Commands
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    # Command logic here

@app.on_message(filters.command("post") & filters.private)
async def post_command(client, message):
    # Post command logic here

@app.on_message(filters.command("rename") & filters.private)
async def rename_command(client, message):
    # Rename command logic here

@app.on_message(filters.command("status") & filters.private)
async def status_command(client, message):
    # Status command logic here

@app.on_message(filters.command("log") & filters.private)
async def log_command(client, message):
    # Log command logic here

@app.on_message(filters.photo | filters.document | filters.video | filters.audio | filters.sticker | filters.text)
async def handle_message(client, message):
    await post_to_channels(client, message)
    await log_to_channel(client, f"Posted message from {message.from_user.username}: {message.text}")

# Periodic tasks
async def periodic_tasks():
    while True:
        now = datetime.now(pytz.timezone('Asia/Kolkata'))
        if now.hour == 9 and now.minute == 0:
            await app.send_message(LOG_CHANNEL_ID, "Good morning message")
        if now.hour == 21 and now.minute == 0:
            await app.send_message(LOG_CHANNEL_ID, "Good night message")
        await asyncio.sleep(60)

async def main():
    await app.start()
    await periodic_tasks()

if __name__ == "__main__":
    app.run(main())
