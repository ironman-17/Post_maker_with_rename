import logging
import sys
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI, LOG_CHANNEL_ID, POST_CHANNELS, TIMEZONE
from utils.helpers import get_greeting, handle_photo, post_to_channels, log_to_channel
from datetime import datetime
import pytz

# Setup logging to stdout
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Command to start the bot
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    await message.reply(get_greeting())

# Command to post to all channels
@app.on_message(filters.command("post") & filters.private)
async def post_command(client, message: Message):
    text = message.text.split(None, 1)[1] if len(message.text.split(None, 1)) > 1 else ''
    await post_to_channels(client, text)
    await message.reply("Posted to all channels.")

# Command to rename files (placeholder, needs implementation)
@app.on_message(filters.command("rename") & filters.private)
async def rename_command(client, message: Message):
    await message.reply("File renaming feature is not yet implemented.")

# Command to check bot status
@app.on_message(filters.command("status") & filters.private)
async def status_command(client, message: Message):
    await message.reply("Bot is running smoothly.")

# Command to log a message to the log channel
@app.on_message(filters.command("log") & filters.private)
async def log_command(client, message: Message):
    log_message = "Bot log: " + get_greeting()
    await log_to_channel(client, log_message)
    await message.reply("Logged to the channel.")

# Handle all private messages
@app.on_message(filters.private)
async def handle_all_messages(client, message: Message):
    await handle_photo(client, message)

# Periodic tasks for scheduled messages
async def periodic_tasks():
    while True:
        now = datetime.now(pytz.timezone(TIMEZONE))
        if now.hour == 9 and now.minute == 0:
            await app.send_message(LOG_CHANNEL_ID, "Good morning message")
        if now.hour == 21 and now.minute == 0:
            await app.send_message(LOG_CHANNEL_ID, "Good night message")
        await asyncio.sleep(60)  # Check every minute

# Main function to run the bot
async def main():
    await app.start()
    logger.info("Bot started.")
    await periodic_tasks()

if __name__ == "__main__":
    try:
        asyncio.run(main())  # Run the main function
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        app.stop()  # Ensure the app stops on exit
