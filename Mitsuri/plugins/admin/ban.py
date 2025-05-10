from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("ban") & filters.group)
async def ban_user(client: Client, message: Message):
    """
    /ban command handler.
    Allows admins to ban a user from the group.
    """
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to the user's message to ban them.")
        return

    user_to_ban = message.reply_to_message.from_user
    chat_id = message.chat.id

    try:
        # Ban the user
        await client.kick_chat_member(chat_id, user_to_ban.id)
        await message.reply_text(f"✅ <b>{user_to_ban.first_name}</b> has been banned from the group.")
    except Exception as e:
        await message.reply_text(f"❌ Failed to ban the user. Error: {e}")
