from time import time
from pyrogram import Client
from pyrogram.types import Message

# Cache to store last message timestamps
user_last_message = {}


async def throttle_user(client: Client, message: Message, cooldown: int = 5):
    """
    Throttle messages from users to prevent spam.
    :param client: Pyrogram client
    :param message: Incoming message
    :param cooldown: Cooldown period in seconds
    """
    user_id = message.from_user.id
    current_time = time()

    if user_id in user_last_message:
        last_message_time = user_last_message[user_id]
        if current_time - last_message_time < cooldown:
            await message.reply_text(
                f"⏳ Please wait {int(cooldown - (current_time - last_message_time))} seconds before sending another message."
            )
            return False

    user_last_message[user_id] = current_time
    return True
