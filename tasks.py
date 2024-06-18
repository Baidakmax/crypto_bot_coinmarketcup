import logging
from aiogram import Bot
from config import API_TOKEN
from database import get_subscriber
from parse import fetch_crypto_prices

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)


async def send_daily_updates():
    """Sends daily updates to all subscribers."""
    try:
        subscribers = get_subscriber()
        crypto_data = fetch_crypto_prices()
        response_message = "\n".join([
            f"{item['name']}: {item['price']} "
            f"(Volume: {item['volume']}, "
            f"Market Cap: {item['market_cap']})" for item in crypto_data])
        for user_id in subscribers:
            await bot.send_message(user_id, response_message)
    except Exception as e:
        logging.error(f"Error while sending daily updates: {e}")