import logging
from datetime import datetime
from pyrogram.types import Message

# Set up logging
logging.basicConfig(
    filename="logs/mitsuri.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


async def log_message(message: Message):
    """
    Log incoming messages to a file.
    :param message: Incoming message
    """
    user = message.from_user
    chat = message.chat
    log_entry = (
        f"{datetime.utcnow()} - User: {user.id} ({user.first_name}) "
        f"in Chat: {chat.id} ({chat.title if chat.title else 'Private'}) - Message: {message.text}"
    )
    logging.info(log_entry)
