import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from ..config import Config


@Client.on_message(filters.command("weather") & filters.private)
async def get_weather(client: Client, message: Message):
    """
    /weather command handler.
    Fetches real-time weather information for a given city.
    """
    if len(message.command) < 2:
        await message.reply_text(
            "❌ Usage: /weather <city_name>\n"
            "Example: /weather Tokyo"
        )
        return

    city_name = " ".join(message.command[1:])
    api_key = Config.API_KEYS.get("openweather")
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    try:
        response = requests.get(base_url, params={
            "q": city_name,
            "appid": api_key,
            "units": "metric"
        })
        data = response.json()

        if data["cod"] != 200:
            await message.reply_text(f"❌ Error: {data['message']}")
            return

        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        await message.reply_text(
            f"🌤️ <b>Weather in {city_name}</b> 🌤️\n\n"
            f"🌡️ Temperature: {temp}°C (Feels like {feels_like}°C)\n"
            f"☁️ Condition: {weather}\n"
            f"💧 Humidity: {humidity}%\n"
            f"🌬️ Wind Speed: {wind_speed} m/s"
        )
    except Exception as e:
        await message.reply_text(f"❌ Failed to fetch weather. Error: {e}")
