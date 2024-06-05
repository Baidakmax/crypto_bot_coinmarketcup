import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import API_TOKEN
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from parse import fetch_crypto_prices
from database import init_db, get_subscriber, remove_subscriber, add_subscriber

#   Configuring logging
logging.basicConfig(level=logging.INFO)

# Initialising the bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Database initialisation
init_db()


# Command start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm a data parsing bot.")


# Command prices
@dp.message(Command("prices"))
async def get_prices(message: types.Message):
    crypto_data = fetch_crypto_prices()
    response_message = "\n".join(
        [f"{item['name']}: {item['price']} (Volume: {item['volume']}, Market Cap: {item['market_cap']})" for item in
         crypto_data])
    await message.reply(response_message)


#  Command subscribe
@dp.message(Command("subscribe"))
async def subscribe(message: types.Message):
    user_id = message.from_user.id
    add_subscriber(user_id)
    await message.reply("You are subscribed to daily updates on cryptocurrency rates.")


# Command unsubscribe
@dp.message(Command("unsubscribe"))
async def unsubscribe(message: types.Message):
    user_id = message.from_user.id
    remove_subscriber(user_id)
    await message.reply("You're unsubscribed from daily updates on cryptocurrency rates.")


# Function for sending daily notifications
async def send_daily_updates():
    subscribes = get_subscriber()
    crypto_data = fetch_crypto_prices()
    responce_message = "\n".join([
        f"{item['name']}: {item['price']} "
        f"(Volume: {item['volume']}, "
        f"Market Cap: {item['market_cap']})" for item in crypto_data])
    for user_id in subscribes:
        await bot.send_message(user_id, responce_message)


# Starting bot
async def main():
    # task scheduler configuration
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_updates, 'interval', hours=24)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
