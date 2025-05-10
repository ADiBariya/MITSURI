from functools import wraps
from time import time
from pyrogram.types import Message

cooldown_cache = {}


def cooldown(seconds: int):
    """
    Decorator to rate-limit commands.
    :param seconds: Cooldown duration in seconds
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(client, message: Message, *args, **kwargs):
            user_id = message.from_user.id
            current_time = time()

            if user_id in cooldown_cache:
                last_used = cooldown_cache[user_id]
                if current_time - last_used < seconds:
                    remaining = seconds - (current_time - last_used)
                    await message.reply_text(f"⏳ Please wait {int(remaining)}s before using this command again.")
                    return

            cooldown_cache[user_id] = current_time
            return await func(client, message, *args, **kwargs)

        return wrapper

    return decorator
