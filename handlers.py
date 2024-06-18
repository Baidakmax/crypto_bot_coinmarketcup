from aiogram import types, Dispatcher, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from keyboards import get_crypto_buttons
from parse import fetch_crypto_prices, fetch_crypto_by_name_first_ten, fetch_crypto_by_name_11_to_100
from database import add_subscriber, remove_subscriber
from state import CryptoStates


async def send_welcome(message: types.Message):
    """
    Sends a welcome message with instructions on how to use the bot.

    Args:
        message (types.Message): Incoming message with the command.
    """
    await message.reply(
        "Hi!\nI'm CryptoBot!\nSend /prices to get the current top 10 crypto prices.\n"
        "Send /top5 to get information about the top 5 cryptocurrencies.\n"
        "Send /search_10 to search for any cryptocurrency by name.\n"
        "Send /search_100 to search for any cryptocurrency from 11 to 100 by name.\n"
        "Send /subscribe to subscribe to daily updates.\n"
        "Send /unsubscribe to unsubscribe from daily updates."
    )


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


async def process_top5_callback(callback_query: types.CallbackQuery, bot: Bot):
    """
    Processes the callback query from the top 5 cryptocurrency buttons.

    Args:
        callback_query (types.CallbackQuery): Incoming callback query.
        bot: Bot
    """
    crypto_name = callback_query.data.split("top5_")[1]
    data = fetch_crypto_prices()
    if not data:
        await bot.send_message(callback_query.from_user.id, "No data found or parsing failed.")
        return

    crypto = next((item for item in data if item['name'] == crypto_name), None)
    if crypto:
        response = (
            f"Name: {crypto['name']}\n"
            f"Price: {crypto['price']}\n"
            f"Volume: {crypto['volume']}\n"
            f"Market Cap: {crypto['market_cap']}")
        await bot.send_message(callback_query.from_user.id, response)
    else:
        await bot.send_message(callback_query.from_user.id, "Cryptocurrency not found.")


async def ask_for_crypto_name_10(message: types.Message, state: FSMContext):
    """
    Handler for the /search_10 command.
    Prompts the user to enter the name of the cryptocurrency they want to search in the top 10.

    Args:
        message (types.Message): The message object containing the command.
        state (FSMContext): The FSM context for managing states.
    """
    await message.answer("Enter the name of the cryptocurrency you want to search (Top 10):")
    await state.set_state(CryptoStates.waiting_for_crypto_name_10)


async def search_crypto_by_name_10(message: types.Message, state: FSMContext):
    """
        Handler for searching a cryptocurrency in the top 10 by name.
        Fetches and returns the cryptocurrency information based on user input.

        Args:
            message (types.Message): The message object containing the user's response.
            state (FSMContext): The FSM context for managing states.
        """
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


async def ask_for_crypto_name_100(message: types.Message, state: FSMContext):
    """
        Handler for the /search_100 command.
        Prompts the user to enter the name of the cryptocurrency they want to search in the rank 11-100.

        Args:
            message (types.Message): The message object containing the command.
            state (FSMContext): The FSM context for managing states.
        """
    await message.answer("Enter the name of the cryptocurrency you want to search (Rank 11-100):")
    await state.set_state(CryptoStates.waiting_for_crypto_name_100)


async def search_crypto_by_name_100(message: types.Message, state: FSMContext):
    """
        Handler for searching a cryptocurrency ranked 11-100 by name.
        Fetches and returns the cryptocurrency information based on user input.

        Args:
            message (types.Message): The message object containing the user's response.
            state (FSMContext): The FSM context for managing states.
    """
    crypto_name = message.text.strip()
    crypto = fetch_crypto_by_name_11_to_100(crypto_name)
    if crypto:
        await message.answer(f"Name: {crypto['name']}\nPrice: {crypto['price']}")
    else:
        await message.answer("Cryptocurrency not found in the ranks 11-100. "
                             "Please check the name and try again /search_100.")
    await state.clear()


async def subscribe(message: types.Message):
    """ Adds the user to the list of subscribers for daily updates. """
    user_id = message.from_user.id
    add_subscriber(user_id)
    await message.reply("You are subscribed to daily updates on cryptocurrency rates.")


async def unsubscribe(message: types.Message):
    """ Removes the user from the list of subscribers for daily updates."""
    user_id = message.from_user.id
    remove_subscriber(user_id)
    await message.reply("You're unsubscribed from daily updates on cryptocurrency rates.")


def register_handlers(dp: Dispatcher, bot: Bot):
    """
    Registers all the handlers for the Telegram bot.

    Args:
        dp (Dispatcher): The Dispatcher object from aiogram used to register handlers.
        bot (Bot): The Bot object from aiogram used to interact with the Telegram API.

    Handlers registered:
        - send_welcome: Handles the /start and /help commands to welcome the user.
        - send_prices: Handles the /prices command to send current cryptocurrency prices.
        - send_menu: Handles the /top5 command to display the top 5 cryptocurrencies.
        - process_top5_callback: Handles callbacks for the top 5 cryptocurrency buttons.
        - ask_for_crypto_name_10: Handles the /search_10 command to prompt the user for a cryptocurrency name within the top 10.
        - search_crypto_by_name_10: Handles user input for searching a cryptocurrency within the top 10.
        - ask_for_crypto_name_100: Handles the /search_100 command to prompt the user for a cryptocurrency name within the top 100.
        - search_crypto_by_name_100: Handles user input for searching a cryptocurrency within the top 100.
        - subscribe: Handles the /subscribe command to subscribe the user for daily updates.
        - unsubscribe: Handles the /unsubscribe command to unsubscribe the user from daily updates.
    """
    dp.message.register(send_welcome, Command("start", "help"))
    dp.message.register(send_prices, Command("prices"))
    dp.message.register(send_menu, Command("top5"))
    dp.callback_query.register(process_top5_callback,
                                       lambda callback_query: callback_query.data.startswith("top5_"))
    dp.message.register(ask_for_crypto_name_10, Command("search_10"))
    dp.message.register(search_crypto_by_name_10, CryptoStates.waiting_for_crypto_name_10)
    dp.message.register(ask_for_crypto_name_100, Command("search_100"))
    dp.message.register(search_crypto_by_name_100, CryptoStates.waiting_for_crypto_name_100)
    dp.message.register(subscribe, Command("subscribe"))
    dp.message.register(unsubscribe, Command("unsubscribe"))