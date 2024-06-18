import logging
import asyncio
from aiogram import Bot, Dispatcher

from config import API_TOKEN
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import init_db
from handlers import register_handlers
from tasks import send_daily_updates


# Configuring logging
logging.basicConfig(level=logging.INFO)

# Initialising the bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Database initialisation
init_db()


# Starting bot
async def main():
    """
    task scheduler configuration
    """
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_updates, 'interval', hours=1)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    register_handlers(dp, bot)
    asyncio.run(main())
