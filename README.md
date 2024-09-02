# Post_maker_with_rename

## Description

This project is a Telegram bot that supports posting to multiple channels, handling messages, and logging.

## Setup

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd telegram_bot_project
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure the bot:**

    Edit `config.py` and add your API ID, API hash, bot token, MongoDB URI, log channel ID, post channel IDs, and timezone.

4. **Run the bot:**

    ```bash
    python bot.py
    ```

## Features

- Greetings based on the time of day
- Post messages to multiple channels
- File renaming feature (to be implemented)
- Logging functionality
- Error handling


## Handles commands: 

- start
- post
- rename
- status
- log
