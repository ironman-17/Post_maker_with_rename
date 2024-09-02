from pyrogram import filters
from modules.commands import register_commands
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.helpers import get_greeting, handle_photo, post_to_channels, log_to_channel

def register_commands(app):

    @app.on_message(filters.command("start") & filters.private)
    async def start_command(client, message: Message):
        # Greeting message
        greeting = get_greeting()
        
        # Buttons configuration
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Post", callback_data="post")],
                [InlineKeyboardButton("Rename", callback_data="rename")],
                [InlineKeyboardButton("Status", callback_data="status")],
                [InlineKeyboardButton("Log", callback_data="log")]
            ]
        )
        
        # Send greeting with buttons
        await message.reply(greeting, reply_markup=keyboard)

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

    @app.on_message(filters.private)
    async def handle_all_messages(client, message: Message):
        await handle_photo(client, message)

    # Optional: Handle button presses
    @app.on_callback_query()
    async def handle_callback_query(client, callback_query):
        data = callback_query.data

        if data == "post":
            await callback_query.message.reply("Post button pressed.")
            # Handle post logic here
        elif data == "rename":
            await callback_query.message.reply("Rename button pressed.")
            # Handle rename logic here
        elif data == "status":
            await callback_query.message.reply("Status button pressed.")
            # Handle status logic here
        elif data == "log":
            await callback_query.message.reply("Log button pressed.")
            # Handle log logic here
