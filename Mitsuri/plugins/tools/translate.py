from pyrogram import Client, filters
from pyrogram.types import Message
from googletrans import Translator


@Client.on_message(filters.command("translate") & filters.private)
async def translate_text(client: Client, message: Message):
    """
    /translate command handler.
    Translates user-provided text into the desired language.
    """
    translator = Translator()

    if len(message.command) < 3:
        await message.reply_text(
            "❌ Usage: /translate <language_code> <text>\n"
            "Example: /translate en Hola Mundo (Translate 'Hola Mundo' to English)"
        )
        return

    target_language = message.command[1]
    text_to_translate = " ".join(message.command[2:])

    try:
        translated = translator.translate(text_to_translate, dest=target_language)
        await message.reply_text(
            f"🌐 <b>Translation</b> 🌐\n\n"
            f"Original: {text_to_translate}\n"
            f"Translated: {translated.text}"
        )
    except Exception as e:
        await message.reply_text(
            f"❌ Failed to translate. Error: {e}"
        )
