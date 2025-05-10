from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("calc") & filters.private)
async def calculate_expression(client: Client, message: Message):
    """
    /calc command handler.
    Evaluates mathematical expressions provided by the user.
    """
    if len(message.command) < 2:
        await message.reply_text(
            "❌ Usage: /calc <expression>\n"
            "Example: /calc 2 + 2 * (3)"
        )
        return

    expression = " ".join(message.command[1:])
    try:
        result = eval(expression)
        await message.reply_text(
            f"🧮 <b>Calculator</b> 🧮\n\n"
            f"Expression: <code>{expression}</code>\n"
            f"Result: <b>{result}</b>"
        )
    except Exception as e:
        await message.reply_text(
            f"❌ Failed to evaluate expression. Error: {e}"
        )
