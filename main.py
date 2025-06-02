import asyncio
import sys

from bot.loader import bot, dp
from bot.handlers import user

async def main():
    dp.include_router(user.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())