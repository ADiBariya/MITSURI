from pyrogram.types import Message

# Blacklist for users and words
blacklisted_users = set()
blacklisted_words = set()


async def check_blacklist(message: Message):
    """
    Check if a message or user is blacklisted.
    :param message: Incoming message
    """
    user_id = message.from_user.id
    text = message.text or ""

    if user_id in blacklisted_users:
        await message.reply_text("❌ You are blacklisted from using this bot.")
        return False

    for word in blacklisted_words:
        if word in text.lower():
            await message.reply_text(f"❌ Your message contains a blacklisted word: {word}")
            return False

    return True
