import asyncio

from loader import dp, bot, on_startup_bot, stop_bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup():
    # Bot ishga tushganida kerakli obyektlarni olish
    await on_startup_bot()

    # Birlamchi komandalar (/star va /help)
    await set_default_commands()

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify()


async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(stop_bot)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
