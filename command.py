from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.helpers import get_greeting, handle_photo, post_to_channels, log_to_channel

def register_commands(app):
    # Common keyboard markup for all messages
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Start", callback_data="start")],
        [InlineKeyboardButton("Post", callback_data="post")],
        [InlineKeyboardButton("Rename", callback_data="rename")],
        [InlineKeyboardButton("Status", callback_data="status")],
        [InlineKeyboardButton("Log", callback_data="log")]
    ])
    
    @app.on_message(filters.command("start") & filters.private)
    async def start_command(client, message: Message):
        await message.reply(get_greeting(), reply_markup=keyboard)

    @app.on_message(filters.command("post") & filters.private)
    async def post_command(client, message: Message):
        text = message.text.split(None, 1)[1] if len(message.text.split(None, 1)) > 1 else ''
        await post_to_channels(client, text)
        await message.reply("Posted to all channels.", reply_markup=keyboard)

    @app.on_message(filters.command("rename") & filters.private)
    async def rename_command(client, message: Message):
        # Implement file renaming logic here
        await message.reply("Rename feature will be implemented here.", reply_markup=keyboard)

    @app.on_message(filters.command("status") & filters.private)
    async def status_command(client, message: Message):
        await message.reply("Bot is running smoothly.", reply_markup=keyboard)

    @app.on_message(filters.command("log") & filters.private)
    async def log_command(client, message: Message):
        log_message = "Bot log: " + get_greeting()
        await log_to_channel(client, log_message)
        await message.reply("Logged to the channel.", reply_markup=keyboard)

    @app.on_message(filters.private)
    async def handle_all_messages(client, message: Message):
        await handle_photo(client, message)
        await message.reply("Photo handled.", reply_markup=keyboard)

    @app.on_callback_query()
    async def button_click(client, callback_query):
        data = callback_query.data
        if data == "start":
            await start_command(client, callback_query.message)
        elif data == "post":
            await post_command(client, callback_query.message)
        elif data == "rename":
            await rename_command(client, callback_query.message)
        elif data == "status":
            await status_command(client, callback_query.message)
        elif data == "log":
            await log_command(client, callback_query.message)
        await callback_query.answer()  # Acknowledge the callback
