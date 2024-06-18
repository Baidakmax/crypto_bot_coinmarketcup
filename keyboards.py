from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from parse import fetch_crypto_prices


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




