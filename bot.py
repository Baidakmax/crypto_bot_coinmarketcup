import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import UNSET_PARSE_MODE
from config import API_TOKEN

#   Configuring logging
logging.basicConfig(level=logging.INFO)

# Initialising the bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Command start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm a data parsing bot.")


# Starting bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

