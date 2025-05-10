from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command("settings") & filters.private)
async def settings_command(client: Client, message: Message):
    """
    /settings command handler.
    Displays a polished settings menu with interactive buttons for customization.
    """
    # Settings menu text
    settings_text = (
        "⚙️ <b>Settings Menu</b> ⚙️\n\n"
        "Customize your preferences to make Mitsuri work better for you 🌸.\n\n"
        "🔹 Enable or disable notifications.\n"
        "🔹 Change themes to match your style.\n"
        "🔹 Manage privacy settings.\n\n"
        "✨ Use the buttons below to navigate settings options."
    )

    # Inline keyboard for settings options
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔔 Notifications", callback_data="settings_notifications")],
        [InlineKeyboardButton("🎨 Themes", callback_data="settings_themes")],
        [InlineKeyboardButton("🔒 Privacy", callback_data="settings_privacy")],
        [InlineKeyboardButton("🔙 Back to Start", callback_data="start_menu")],
    ])

    # Send the settings menu
    await message.reply_text(
        settings_text,
        reply_markup=keyboard
    )


@Client.on_callback_query(filters.regex(r"settings_notifications"))
async def settings_notifications(client, callback_query):
    """
    Callback query handler for Notifications settings.
    Allows the user to enable or disable notifications.
    """
    notifications_text = (
        "🔔 <b>Notification Settings</b> 🔔\n\n"
        "Manage your notification preferences:\n"
        "🔹 Enable notifications to stay updated.\n"
        "🔹 Disable notifications for a quieter experience.\n\n"
        "✨ Use the buttons below to toggle notifications."
    )

    # Inline keyboard to toggle notifications
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Enable", callback_data="notifications_enable")],
        [InlineKeyboardButton("❌ Disable", callback_data="notifications_disable")],
        [InlineKeyboardButton("🔙 Back to Settings", callback_data="settings_menu")],
    ])

    await callback_query.message.edit_text(
        notifications_text,
        reply_markup=keyboard
    )


@Client.on_callback_query(filters.regex(r"notifications_enable"))
async def notifications_enable(client, callback_query):
    """
    Callback query handler to enable notifications.
    """
    # Simulate enabling notifications (logic can be added later)
    await callback_query.answer("✅ Notifications enabled!")
    await settings_notifications(client, callback_query)


@Client.on_callback_query(filters.regex(r"notifications_disable"))
async def notifications_disable(client, callback_query):
    """
    Callback query handler to disable notifications.
    """
    # Simulate disabling notifications (logic can be added later)
    await callback_query.answer("❌ Notifications disabled!")
    await settings_notifications(client, callback_query)


@Client.on_callback_query(filters.regex(r"settings_themes"))
async def settings_themes(client, callback_query):
    """
    Callback query handler for Themes settings.
    Allows the user to select a theme.
    """
    themes_text = (
        "🎨 <b>Theme Settings</b> 🎨\n\n"
        "Choose a theme to match your style:\n"
        "🔹 Light Theme - Bright and clear.\n"
        "🔹 Dark Theme - Sleek and easy on the eyes.\n\n"
        "✨ Use the buttons below to select a theme."
    )

    # Inline keyboard to select themes
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌞 Light Theme", callback_data="theme_light")],
        [InlineKeyboardButton("🌑 Dark Theme", callback_data="theme_dark")],
        [InlineKeyboardButton("🔙 Back to Settings", callback_data="settings_menu")],
    ])

    await callback_query.message.edit_text(
        themes_text,
        reply_markup=keyboard
    )


@Client.on_callback_query(filters.regex(r"theme_light"))
async def theme_light(client, callback_query):
    """
    Callback query handler to set the Light Theme.
    """
    # Simulate setting the Light Theme (logic can be added later)
    await callback_query.answer("🌞 Light Theme activated!")
    await settings_themes(client, callback_query)


@Client.on_callback_query(filters.regex(r"theme_dark"))
async def theme_dark(client, callback_query):
    """
    Callback query handler to set the Dark Theme.
    """
    # Simulate setting the Dark Theme (logic can be added later)
    await callback_query.answer("🌑 Dark Theme activated!")
    await settings_themes(client, callback_query)


@Client.on_callback_query(filters.regex(r"settings_privacy"))
async def settings_privacy(client, callback_query):
    """
    Callback query handler for Privacy settings.
    Displays privacy options for the user to manage.
    """
    privacy_text = (
        "🔒 <b>Privacy Settings</b> 🔒\n\n"
        "Manage your privacy settings:\n"
        "🔹 Enable privacy mode to hide your activity.\n"
        "🔹 Disable privacy mode to allow more features.\n\n"
        "✨ Use the buttons below to toggle privacy mode."
    )

    # Inline keyboard to toggle privacy settings
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔐 Enable Privacy Mode", callback_data="privacy_enable")],
        [InlineKeyboardButton("⚪ Disable Privacy Mode", callback_data="privacy_disable")],
        [InlineKeyboardButton("🔙 Back to Settings", callback_data="settings_menu")],
    ])

    await callback_query.message.edit_text(
        privacy_text,
        reply_markup=keyboard
    )


@Client.on_callback_query(filters.regex(r"privacy_enable"))
async def privacy_enable(client, callback_query):
    """
    Callback query handler to enable privacy mode.
    """
    # Simulate enabling privacy mode (logic can be added later)
    await callback_query.answer("🔐 Privacy mode enabled!")
    await settings_privacy(client, callback_query)


@Client.on_callback_query(filters.regex(r"privacy_disable"))
async def privacy_disable(client, callback_query):
    """
    Callback query handler to disable privacy mode.
    """
    # Simulate disabling privacy mode (logic can be added later)
    await callback_query.answer("⚪ Privacy mode disabled!")
    await settings_privacy(client, callback_query)


@Client.on_callback_query(filters.regex(r"settings_menu"))
async def settings_menu(client, callback_query):
    """
    Callback query handler to return to the main Settings menu.
    """
    settings_text = (
        "⚙️ <b>Settings Menu</b> ⚙️\n\n"
        "Customize your preferences to make Mitsuri work better for you 🌸.\n\n"
        "🔹 Enable or disable notifications.\n"
        "🔹 Change themes to match your style.\n"
        "🔹 Manage privacy settings.\n\n"
        "✨ Use the buttons below to navigate settings options."
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔔 Notifications", callback_data="settings_notifications")],
        [InlineKeyboardButton("🎨 Themes", callback_data="settings_themes")],
        [InlineKeyboardButton("🔒 Privacy", callback_data="settings_privacy")],
        [InlineKeyboardButton("🔙 Back to Start", callback_data="start_menu")],
    ])

    await callback_query.message.edit_text(
        settings_text,
        reply_markup=keyboard
    )
