# utils/helpers.py

from datetime import datetime
from pytz import timezone
from pyrogram import Client

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
      
