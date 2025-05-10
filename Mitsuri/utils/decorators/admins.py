from functools import wraps
from pyrogram.types import Message


def admin_required(func):
    """
    Decorator to ensure a command is executed only by admins.
    :param func: Command function
    """

    @wraps(func)
    async def wrapper(client, message: Message, *args, **kwargs):
        if not message.from_user:
            await message.reply_text("❌ This command can only be used by admins.")
            return

        user = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status not in ("administrator", "creator"):
            await message.reply_text("❌ You need to be an admin to use this command.")
            return

        return await func(client, message, *args, **kwargs)

    return wrapper
