from functools import wraps
from pyrogram.errors import RPCError
from pyrogram.types import Message


def handle_errors(func):
    """
    Decorator to handle errors gracefully.
    :param func: Command function
    """

    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except RPCError as e:
            await message.reply_text(f"❌ An error occurred: {str(e)}")
        except Exception as e:
            await message.reply_text("❌ Something went wrong. Please try again later.")
            raise e

    return wrapper
