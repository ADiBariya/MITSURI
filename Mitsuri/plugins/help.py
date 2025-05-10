from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command("help") & filters.private)
async def help_command(client: Client, message: Message):
    """
    /help command handler.
    Provides a polished help menu with inline buttons for different categories.
    """
    user = message.from_user

    # Help text
    help_text = (
        f"📖 <b>Help Menu</b> 📖\n\n"
        f"Hello, <b>{user.first_name}</b>! Here’s how you can use <b>Mitsuri</b> 🌸:\n\n"
        "🔹 Use the buttons below to explore different help topics.\n"
        "🔹 If you need further assistance, check out the Support section (/start > Support).\n\n"
        "✨ Let’s get started!"
    )

    # Inline keyboard buttons for different help categories
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 General Commands", callback_data="help_general")],
        [InlineKeyboardButton("🛠️ Admin Commands", callback_data="help_admin")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="help_settings")],
        [InlineKeyboardButton("🔙 Back to Start", callback_data="start_menu")],
    ])

    # Send the help menu
    await message.reply_text(
        help_text,
        reply_markup=keyboard
    )


@Client.on_callback_query(filters.regex(r"help_general"))
async def help_general(client, callback_query):
    """
    Callback query handler for General Commands help.
    Displays a list of general commands and their descriptions.
    """
    general_help_text = (
        "📋 <b>General Commands</b> 📋\n\n"
        "Here are the commands you can use:\n"
        "🔹 /start - Start the bot and see the welcome menu.\n"
        "🔹 /help - Display this help menu.\n"
        "🔹 /settings - Manage your preferences.\n"
        "🔹 /about - Learn more about Mitsuri.\n\n"
        "✨ Explore and enjoy!"
    )
    await callback_query.message.edit_text(
        general_help_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Help", callback_data="help_menu")]
        ])
    )


@Client.on_callback_query(filters.regex(r"help_admin"))
async def help_admin(client, callback_query):
    """
    Callback query handler for Admin Commands help.
    Displays a list of admin commands and their descriptions.
    """
    admin_help_text = (
        "🛠️ <b>Admin Commands</b> 🛠️\n\n"
        "These commands are for bot admins only:\n"
        "🔹 /ban - Ban a user from the chat.\n"
        "🔹 /mute - Mute a user in the chat.\n"
        "🔹 /unmute - Unmute a user in the chat.\n"
        "🔹 /announce - Make an announcement in the chat.\n\n"
        "✨ Ensure you have the required permissions!"
    )
    await callback_query.message.edit_text(
        admin_help_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Help", callback_data="help_menu")]
        ])
    )


@Client.on_callback_query(filters.regex(r"help_settings"))
async def help_settings(client, callback_query):
    """
    Callback query handler for Settings Commands help.
    Displays a list of settings commands and their descriptions.
    """
    settings_help_text = (
        "⚙️ <b>Settings</b> ⚙️\n\n"
        "Manage your preferences using these commands:\n"
        "🔹 /settings - Open the settings menu.\n"
        "🔹 /set_notifications - Enable/disable notifications.\n"
        "🔹 /set_theme - Choose your preferred theme.\n\n"
        "✨ Customize Mitsuri to suit your needs!"
    )
    await callback_query.message.edit_text(
        settings_help_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Help", callback_data="help_menu")]
        ])
    )


@Client.on_callback_query(filters.regex(r"help_menu"))
async def help_menu(client, callback_query):
    """
    Callback query handler to return to the main Help menu.
    """
    user = callback_query.from_user
    help_text = (
        f"📖 <b>Help Menu</b> 📖\n\n"
        f"Hello again, <b>{user.first_name}</b>! Here’s how you can use <b>Mitsuri</b> 🌸:\n\n"
        "🔹 Use the buttons below to explore different help topics.\n"
        "🔹 If you need further assistance, check out the Support section (/start > Support).\n\n"
        "✨ Let’s get started!"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 General Commands", callback_data="help_general")],
        [InlineKeyboardButton("🛠️ Admin Commands", callback_data="help_admin")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="help_settings")],
        [InlineKeyboardButton("🔙 Back to Start", callback_data="start_menu")],
    ])
    await callback_query.message.edit_text(
        help_text,
        reply_markup=keyboard
    )
