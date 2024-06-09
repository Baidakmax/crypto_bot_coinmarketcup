import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import API_TOKEN
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from parse import fetch_crypto_prices, fetch_crypto_by_name_first_ten, fetch_crypto_by_name_11_to_100
from database import init_db, get_subscriber, remove_subscriber, add_subscriber

#   Configuring logging
logging.basicConfig(level=logging.INFO)

# Initialising the bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()



# Define FSM states
class CryptoStates(StatesGroup):
    waiting_for_crypto_name_10 = State()
    waiting_for_crypto_name_100 = State()

# Database initialisation
init_db()


@dp.message(Command('start', 'help'))
async def send_welcome(message: types.Message):
    """
    Sends a welcome message with instructions on how to use the bot.

    Args:
        message (types.Message): Incoming message with the command.
    """
    await message.reply(
        "Hi!\nI'm CryptoBot!\nSend /prices to get the current top 10 crypto prices.\n"
        "Send /top to get information about the top 5 cryptocurrencies.\n"
        "Send /search_10 to search for any cryptocurrency by name.\n"
        "Send /search_100 to search for any cryptocurrency from 11 to 100 by name.\n"
        "Send /subscribe to subscribe to daily updates.\n"
        "Send /unsubscribe to unsubscribe from daily updates."
    )


@dp.message(Command('prices'))
async def send_prices(message: types.Message):
    """
    Sends a message with the current prices, volumes, and market caps of the top 10 cryptocurrencies.

    Args:
        message (types.Message): Incoming message with the command.
    """
    data = fetch_crypto_prices()
    if data:
        response = ""
        for item in data:
            response += (
                f"{item['name']}, Price: {item['price']}, Volume: {item['volume']}, Market Cap: {item['market_cap']}\n"
                f"---------------------------------\n")
        await message.reply(response)
    else:
        await message.reply("No data found or parsing failed.")


# Function to generate inline keyboard with top 5 cryptocurrencies
def get_crypto_buttons():
    """
    Generates an inline keyboard with buttons for the top 5 cryptocurrencies.

    Returns:
        InlineKeyboardMarkup: Inline keyboard with buttons for the top 5 cryptocurrencies.
    """
    data = fetch_crypto_prices(limit=5)
    if not data:
        return None

    top_5 = data[:5]
    buttons = []
    for crypto in top_5:
        button = InlineKeyboardButton(text=f"{crypto['name']}", callback_data=f"top5_{crypto['name']}")
        buttons.append(button)
    if buttons:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
        return keyboard
    else:
        return None


@dp.message(Command("top"))
async def send_menu(message: types.Message):
    """
    Sends a message with buttons for the top 5 cryptocurrencies.

    Args:
        message (types.Message): Incoming message with the command.
    """
    keyboard = get_crypto_buttons()
    if keyboard:
        await message.reply("Select a cryptocurrency:", reply_markup=keyboard)
    else:
        await message.reply("No data found or parsing failed.")


@dp.callback_query(lambda callback_query: callback_query.data.startswith("top5_"))
async def process_top5_callback(callback_query: types.CallbackQuery):
    """
    Processes the callback query from the top 5 cryptocurrency buttons.

    Args:
        callback_query (types.CallbackQuery): Incoming callback query.
    """
    crypto_name = callback_query.data.split("top5_")[1]
    data = fetch_crypto_prices()
    if not data:
        await bot.send_message(callback_query.from_user.id, "No data found or parsing failed.")
        return

    crypto = next((item for item in data if item['name'] == crypto_name), None)
    if crypto:
        response = (
            f"Name: {crypto['name']}\nPrice: {crypto['price']}\nVolume: {crypto['volume']}\nMarket Cap: {crypto['market_cap']}")
        await bot.send_message(callback_query.from_user.id, response)
    else:
        await bot.send_message(callback_query.from_user.id, "Cryptocurrency not found.")


@dp.message(Command("search_10"))
async def ask_for_crypto_name_10(message: types.Message, state: FSMContext):
    await message.answer("Enter the name of the cryptocurrency you want to search (Top 10):")
    await state.set_state(CryptoStates.waiting_for_crypto_name_10)


@dp.message(CryptoStates.waiting_for_crypto_name_10)
async def search_crypto_by_name_10(message: types.Message, state: FSMContext):
    crypto_name = message.text.strip()
    crypto = fetch_crypto_by_name_first_ten(crypto_name)
    if crypto:
        await message.answer(f"{crypto['name']}\n"
                             f"Price: {crypto['price']}\n"
                             f"Volume: {crypto['volume']}\n"
                             f"Market Cap: {crypto['market_cap']}")
    else:
        await message.answer("Cryptocurrency not found in the Top 10. Please check the name and try again /search_10.")
    await state.clear()


@dp.message(Command("search_100"))
async def ask_for_crypto_name_100(message: types.Message, state: FSMContext):
    await message.answer("Enter the name of the cryptocurrency you want to search (Rank 11-100):")
    await state.set_state(CryptoStates.waiting_for_crypto_name_100)


@dp.message(CryptoStates.waiting_for_crypto_name_100)
async def search_crypto_by_name_100(message: types.Message, state: FSMContext):
    crypto_name = message.text.strip()
    crypto = fetch_crypto_by_name_11_to_100(crypto_name)
    if crypto:
        await message.answer(f"Name: {crypto['name']}\nPrice: {crypto['price']}")
    else:
        await message.answer("Cryptocurrency not found in the ranks 11-100. Please check the name and try again /search_100.")
    await state.clear()




#  Command subscribe
@dp.message(Command("subscribe"))
async def subscribe(message: types.Message):
    """ Adds the user to the list of subscribers for daily updates. """
    user_id = message.from_user.id
    add_subscriber(user_id)
    await message.reply("You are subscribed to daily updates on cryptocurrency rates.")


# Command unsubscribe
@dp.message(Command("unsubscribe"))
async def unsubscribe(message: types.Message):
    """ Removes the user from the list of subscribers for daily updates."""
    user_id = message.from_user.id
    remove_subscriber(user_id)
    await message.reply("You're unsubscribed from daily updates on cryptocurrency rates.")


# Function for sending daily notifications
async def send_daily_updates():
    """Sends daily updates to all subscribers."""
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
    asyncio.run(main())
