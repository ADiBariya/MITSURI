from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import timedelta


@Client.on_message(filters.command("mute") & filters.group)
async def mute_user(client: Client, message: Message):
    """
    /mute command handler.
    Allows admins to mute a user in the group for a specified duration.
    """
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to the user's message to mute them.")
        return

    user_to_mute = message.reply_to_message.from_user
    chat_id = message.chat.id

    # Extract mute duration from the command
    try:
        _, duration = message.text.split(maxsplit=1)
        duration = int(duration)
    except ValueError:
        await message.reply_text("❌ Invalid duration. Usage: /mute <duration_in_minutes>")
        return
    except IndexError:
        duration = 10  # Default to 10 minutes if no duration is provided

    try:
        # Mute the user for the specified duration
        until_date = timedelta(minutes=duration)
        await client.restrict_chat_member(
            chat_id,
            user_to_mute.id,
            permissions={"can_send_messages": False},
            until_date=until_date
        )
        await message.reply_text(f"✅ <b>{user_to_mute.first_name}</b> has been muted for {duration} minutes.")
    except Exception as e:
        await message.reply_text(f"❌ Failed to mute the user. Error: {e}")
