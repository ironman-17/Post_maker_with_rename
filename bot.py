import logging
import sys
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

# Import the function to register commands
from commands import register_commands

# Setup logging to stdout
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Register all the command handlers
register_commands(app)

if __name__ == "__main__":
    app.run()
