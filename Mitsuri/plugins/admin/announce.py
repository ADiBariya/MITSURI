from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("announce") & filters.group)
async def announce_message(client: Client, message: Message):
    """
    /announce command handler.
    Allows admins to make announcements in the group.
    """
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide a message to announce. Usage: /announce <message>")
        return

    # Extract the announcement text
    announcement_text = message.text.split(maxsplit=1)[1]

    try:
        # Send the announcement
        await client.send_message(
            chat_id=message.chat.id,
            text=f"📢 <b>Announcement:</b>\n\n{announcement_text}",
            disable_web_page_preview=True
        )
        await message.reply_text("✅ Announcement sent successfully.")
    except Exception as e:
        await message.reply_text(f"❌ Failed to send the announcement. Error: {e}")
