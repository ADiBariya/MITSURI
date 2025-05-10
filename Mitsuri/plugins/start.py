from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    """
    /start command handler.
    Provides a polished welcome message with inline buttons for Updates, Support, and Help.
    """
    user = message.from_user

    # Welcome text
    welcome_text = (
        f"👋 Hello, <b>{user.first_name}</b>! Welcome to <b>Mitsuri</b> 🌸\n\n"
        "I am your advanced assistant bot, here to help you manage tasks, "
        "fetch information, and much more.\n\n"
        "✨ Use the buttons below to explore Updates, get Support, or access Help."
    )

    # Inline keyboard buttons for navigation
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Updates", callback_data="updates_menu")],
        [InlineKeyboardButton("🛠️ Support", callback_data="support_menu")],
        [InlineKeyboardButton("📖 Help", callback_data="help_menu")],
    ])

    # Send the welcome message
    await message.reply_photo(
        photo="https://telegra.ph/file/57c0f9b7c9a947c7c3b65.jpg",  # Mitsuri-themed image
        caption=welcome_text,
        reply_markup=keyboard
    )


@Client.on_callback_query(filters.regex(r"updates_menu"))
async def updates_menu(client, callback_query):
    """
    Callback query handler for the Updates button.
    Displays the latest updates and features of the bot.
    """
    updates_text = (
        "📢 <b>Latest Updates</b> 📢\n\n"
        "✨ <b>Version 2.0 Released!</b>\n"
        "- Improved performance and stability.\n"
        "- Added support for YouTube, Instagram, and Twitter APIs.\n"
        "- Enhanced UI with inline buttons and multimedia support.\n\n"
        "Stay tuned for more updates!"
    )
    await callback_query.message.edit_text(
        updates_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="start_menu")]
        ])
    )


@Client.on_callback_query(filters.regex(r"support_menu"))
async def support_menu(client, callback_query):
    """
    Callback query handler for the Support button.
    Provides links to GitHub issues, Telegram support, or documentation.
    """
    support_text = (
        "🛠️ <b>Support</b> 🛠️\n\n"
        "Need help or found an issue? Here are your options:\n"
        "- 📂 <b>GitHub:</b> Report issues or contribute to the project.\n"
        "- 🤝 <b>Telegram:</b> Join the support group for assistance.\n"
        "- 📚 <b>Docs:</b> Read the documentation for detailed guidance."
    )
    await callback_query.message.edit_text(
        support_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("GitHub", url="https://github.com/ADiBariya/Mitsuri")],
            [InlineKeyboardButton("Telegram Support", url="https://t.me/MitsuriSupport")],
            [InlineKeyboardButton("Docs", url="https://mitsuri-docs.example.com")],
            [InlineKeyboardButton("🔙 Back", callback_data="start_menu")],
        ])
    )


@Client.on_callback_query(filters.regex(r"help_menu"))
async def help_menu(client, callback_query):
    """
    Callback query handler for the Help button.
    Displays detailed help information.
    """
    help_text = (
        "📖 <b>Help Menu</b> 📖\n\n"
        "Use the following commands to interact with me:\n"
        "- /start - Start the bot and see the welcome menu.\n"
        "- /help - Display this help message.\n"
        "- /settings - Manage your preferences.\n\n"
        "If you have any issues, feel free to reach out through the Support menu."
    )
    await callback_query.message.edit_text(
        help_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="start_menu")]
        ])
    )


@Client.on_callback_query(filters.regex(r"start_menu"))
async def start_menu(client, callback_query):
    """
    Callback query handler to return to the start menu.
    """
    user = callback_query.from_user
    welcome_text = (
        f"👋 Hello again, <b>{user.first_name}</b>! Welcome back to <b>Mitsuri</b> 🌸\n\n"
        "Use the buttons below to navigate or type /help to see all commands."
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Updates", callback_data="updates_menu")],
        [InlineKeyboardButton("🛠️ Support", callback_data="support_menu")],
        [InlineKeyboardButton("📖 Help", callback_data="help_menu")],
    ])
    await callback_query.message.edit_text(
        welcome_text,
        reply_markup=keyboard
    )
